# http://index.baidu.com/Interface/Newwordgraph/getLive?wordlist[0]=%


from string import Template


def join_live_url(words):
    # 全国 北京 上海 广州 深圳
    url = 'http://index.baidu.com/Interface/Newwordgraph/getLive?'

    for w in words:
        url += 'wordlist[]=' + str(w) + '&'

    return url



print(join_live_url(['a','b','c','d','e']))
