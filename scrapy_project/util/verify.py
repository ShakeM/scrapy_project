import requests


def bduss(cookies):
    url = 'https://zhidao.baidu.com/ichat/api/chatlist'
    response = requests.get(url, cookies=cookies)
    if "u6210" in response.text:
        return True
    else:
        return False


def bdusses(cookies):
    results = []

    for c in cookies:
        results.append(bduss(c))

    if False in results:
        return False
    else:
        return True

# result = verify_bduss(cookies)
# print(result)
