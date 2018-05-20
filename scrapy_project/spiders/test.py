import json
from collections import Counter

# with open('stock_list.json', 'rb') as f:
#     all_zips = []
#     for line in f.readlines():
#         line = json.loads(line.decode('utf-8'))
#         zips = line['zips']
#         all_zips += zips
#
#
#         # b = map(lambda x: push(x),[a for a in zips])
#
# symbols = list(map(lambda x:x['symbol'], all_zips))
#
# print(len(symbols))
#
# count = Counter(symbols)
# print(count)

# import os
#
# this_folder_path = os.path.dirname(__file__)
# parent_folder_path = os.path.dirname(this_folder_path)
# output_path = os.path.join(parent_folder_path, 'output')
#
# print(os.path.exists(output_path))
#
# if not os.path.exists(output_path):
#     os.mkdir(output_path)


import arrow

print(arrow.now().format('YYYY-MM-DD_HH-mm-ss_X'))