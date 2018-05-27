import json, os

folder_path = os.path.dirname(__file__)
f1_path = os.path.join(folder_path, 'index_2018-05-27_04-00-29__1527364829.json')
f2_path = os.path.join(folder_path, 'stock_2018-05-27_15-05-29__1527404729.json')

words_1 = []
with open(f1_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        words_1.append(json.loads(l)['word'])

words_2 = []
with open(f2_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        words_2.append(json.loads(l)['word'])

# result = list(filter(lambda x: x not in words_1, words_2))
result = list(filter(lambda x: x not in words_2, words_2))
print(result)

