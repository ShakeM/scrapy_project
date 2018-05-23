import requests

cookies = {
    "BDUSS": "0hUWU5oSlVub2RKNjBpSHNESGZoZk9rQVhJLS1SU1JkTFJnbGRVY29sYW1TfnRaSVFBQUFBJCQAAAAAAAAAAAEAAACARy7G1bKzve-~AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKa-01mmvtNZZ;"}


def verify_bduss(cookies):
    url = 'https://zhidao.baidu.com/ichat/api/chatlist'
    response = requests.get(url, cookies=cookies)
    if "u6210" in response.text:
        return True
    else:
        return False


# result = verify_bduss(cookies)
# print(result)
