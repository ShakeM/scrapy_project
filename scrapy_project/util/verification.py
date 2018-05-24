import requests

def verify_bduss(cookies):
    url = 'https://zhidao.baidu.com/ichat/api/chatlist'
    response = requests.get(url, cookies=cookies)
    if "u6210" in response.text:
        return True
    else:
        return False


# result = verify_bduss(cookies)
# print(result)
