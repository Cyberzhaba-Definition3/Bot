def main():
    from PIL import Image
    import json
    import random

    number_of_all = 10000

    all_info = json.load(open("template.json", "r"))
    new_info = [ [] for _ in range(len(all_info.keys()))]
    counter = 0
    for key, layer in all_info.items():
        counter_for_layer = 0
        for item in layer:
            if counter_for_layer == 0:
                diapason = f'1-{int(100*item["rarity"])}'
                new_info[counter].append({diapason: item['name']})
                prev = int(float(diapason.split('-')[1]))
            else:
                diapason = f'{prev+1}-{prev+int(100*item["rarity"])}'
                new_info[counter].append({diapason: item['name']})
                prev = int(float(diapason.split('-')[1]))
            counter_for_layer += 1
        counter += 1


    print(new_info)
    combinations = []    
    counter = 0 
    for _ in range(number_of_all):
        output = []
        for layer in new_info:
            num = random.randint(1, 100)
            for item in layer:
                prob = list(item.keys())[0].split('-')
                if int(prob[0]) <= num <= int(prob[1]):
                    counter += 1
                    output.append(list(item.values())[0])
                    break
        output = ':'.join(output)
        combinations.append(output)
                
    print(combinations)