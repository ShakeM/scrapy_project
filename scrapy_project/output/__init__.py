import requests

url = "https://xueqiu.com/stock/quote_order.json"

querystring = {"page":"15","size":"90","order":"desc","exchange":"CN","stockType":"sha","column":"symbol,name,current,chg,percent,last_close,open,high,low,volume,amount,market_capital,pe_ttm,high52w,low52w,hasexist","orderBy":"percent","_":"1527824619829"}

headers = {
    # 'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
    # 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # 'accept-encoding': "gzip, deflate, br",
    # 'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cookie': "xq_a_token=7023b46a2c20d7b0530b4e9725f7f869c8d16e7d; ",
    # 'cache-control': "no-cache",
    # 'postman-token': "bf262108-d79c-861f-4f20-44b6331ce280"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)