# import requests
#
# url = "https://xueqiu.com/stock/quote_order.json"
#
# querystring = {"page":"15","size":"90","order":"desc","exchange":"CN","stockType":"sha","column":"symbol,name,current,chg,percent,last_close,open,high,low,volume,amount,market_capital,pe_ttm,high52w,low52w,hasexist","orderBy":"percent","_":"1527824619829"}
#
# headers = {
# 'upgrade-insecure-requests': "1",
# 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
# 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# 'accept-encoding': "gzip, deflate, br",
# 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
# 'cookie': "xq_a_token=7023b46a2c20d7b0530b4e9725f7f869c8d16e7d; ",
# 'cache-control': "no-cache",
# 'postman-token': "bf262108-d79c-861f-4f20-44b6331ce280"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

import arrow

stock = {"word": "创业板指", "period": "20180601 08:00:00|20180602 07:00:00",
         "pc": "0,21,28,24,7,40,59,20,15,11,7,6,5,0,1,1,0,0,0,0,0,0,0,1",
         "all": "11,159,324,263,97,335,438,203,80,58,43,27,38,24,18,20,4,6,0,0,4,2,6,11",
         "wise": "11,138,296,239,90,295,379,183,65,47,36,21,33,24,17,19,4,6,0,0,4,2,6,10"}

period = stock['period']
begin = period.split('|')[0]

time_template = 'YYYYMMDD HH:mm:ss'
begin_arrow = arrow.get(begin, time_template)

periods = [begin_arrow.shift(hours=hours).format(time_template) for hours in range(24)]
print(periods)
