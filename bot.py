import telebot
import zipfile
import requests
import os
import config
import messages
import generator


class Bot:
    
    def __init__(self):
        
        self.bot = telebot.TeleBot(config.token)
    
    def mainloop(self):
        
        @self.bot.message_handler(commands = ['start', 'info', 'gen'])
        def commands(msg):
            if msg.text == '/start':
                self.bot.send_message(msg.chat.id, messages.start_message)
            elif msg.text == '/info':
                self.bot.send_message(msg.chat.id, messages.info_message)
                print(f'processing file for {msg.from_user.id}')
                with open('generation.zip', 'rb') as file:
                    self.bot.send_document(msg.chat.id, file)
                    print(f'file sent for {msg.from_user.id}')
            else:
                bot_msg = self.bot.send_message(msg.chat.id, 
                                                'Пожалуйста отправьте сформированный архив\n(Чтобы посмотреть как это сделать напишите /info)')
                self.bot.register_next_step_handler(bot_msg, get_zip)
        
        def get_zip(msg):
            if msg.text == '/info':
                commands('/info')
            else:
                if msg.document.file_name.endswith('.zip'): 
                    file_info = self.bot.get_file(msg.document.file_id)
                    file_user = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path))
                    filename = f'temp/{msg.document.file_id}.zip'
                    with open(filename, 'wb') as file:
                        file.write(file_user.content)
                    self.bot.send_message(msg.chat.id, 'Бот принял файла на обработку, ожидайте...')
                    self.analyse_zip(msg, filename[5:])
                else:
                    self.bot.send_message(msg.chat.id, 'Что-то не так с отправкой файла. Проверьте все и попробуйте ещё раз')
        
        self.bot.polling()
    
    def analyse_zip(self, msg, zip):
        with zipfile.ZipFile(f'temp/{zip}', 'r') as zip_ref:
            zip_ref.extractall(f'unzipped/{zip[:-4]}')
        first_dir = f'unzipped/{zip[:-4]}'
        folder_inside = os.listdir(first_dir)
        result = os.listdir(f'{first_dir}/{folder_inside[0]}')
        if 'template.json' in result and len(result) > 1:
            self.bot.send_message(msg.chat.id, 'Архив проверен. template.json в архиве есть, посторонние файлы тоже имеются.\nПриступаем к генерации')
            os.remove(f'temp/{zip}')
            generator.main(f'{first_dir}/{folder_inside[0]}')

if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()