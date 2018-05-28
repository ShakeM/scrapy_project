import json, os

folder_path = os.path.dirname(__file__)
# f1_path = os.path.join(folder_path, 'index_2018-05-27_04-00-29__1527364829.json')
# f2_path = os.path.join(folder_path, 'index_2018-05-27_22-03-00__1527429780.json')
f2_path = os.path.join(folder_path, 'standard.json')

# words_1 = []
# with open(f1_path, 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for l in lines:
#         words_1.append(json.loads(l)['word'])

words_2 = []
with open(f2_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        words_2.append(json.loads(l)['word'])

# result = list(filter(lambda x: x not in words_1, words_2))
print(words_2)
from collections import Counter
c = Counter()
print(Counter(words_2))

