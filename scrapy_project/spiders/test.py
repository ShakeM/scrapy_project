# http://index.baidu.com/Interface/Newwordgraph/getLive?wordlist[0]=%


from string import Template


def join_live_url(words):
    # 全国 北京 上海 广州 深圳
    url = 'http://index.baidu.com/Interface/Newwordgraph/getLive?'

    for w in words:
        url += 'wordlist[]=' + str(w) + '&'

    return url


print(join_live_url(['a', 'b', 'c', 'd', 'e']))

demo_words = list(range(10))
for i in range(26):
    demo_words.append(chr(i + ord('a')))

five_words = []
for i in range(len(demo_words)):
    five = demo_words[i * 5:i * 5 + 5]
    if not five: break

    five_words.append(five)

print(five_words)

