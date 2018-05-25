from scrapy_project.util import verification
import yagmail
import os
import re
from functools import reduce

cookies = [
    {
        "BDUSS": "1hMlV6ZVl4WnBqd0x5bmF-TWVac1RmRjU3NGFrb1BINVF3RkV0UUlNTi1TfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAA8cC7Gua3B6cvJtcS5ysrCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6-01l-vtNZZU;"},
    {
        "BDUSS": "0hUWU5oSlVub2RKNjBpSHNESGZoZk9rQVhJLS1SU1JkTFJnbGRVY29sYW1TfnRaSVFBQUFBJCQAAAAAAAAAAAEAAACARy7G1bKzve-~AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKa-01mmvtNZZ;"},
    {
        "BDUSS": "ndMNTNmVmZDRWY4V2VvaWNFUzgwT1JMLTl2NGd5V2RLNUR5ZkJUZWtGdDdTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAAncC7GvOHOysT9y6vX0wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHu-01l7vtNZU;"},
    {
        "BDUSS": "k9HRlF4WWNoREkxdXBsUkpIc3g0NnVCQzI4TkdaNlo4MnRVLUcwZHNHbDZTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABURi7GxeHStryqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHq-01l6vtNZf;"},
    {
        "BDUSS": "1h1VlJ0N3RFfjRnU2NGbi1VZnFnfjNVaHRVeWlZMG5mdkRFUnBiMX54ZzRraGxhTVFBQUFBJCQAAAAAAAAAAAEAAAB9b3TJxKb0yYNoucjH2wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgF8lk4BfJZZ;"},
    {
        "BDUSS": "VLeGk0UFRFaU9tLUhDQmFaMWJFd2ktQ0k3fkxJWUR5TnNETHYwV25wczVraGxhTVFBQUFBJCQAAAAAAAAAAAEAAABWTnTJb2u-o9bZyuYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkF8lk5BfJZbn;"},
    {
        "BDUSS": "l0TkR-fms3OTBtdzZNcn4tVUZWc0xlem5XUkEzYzBlMTJEbWw1LVlSN2RraGxhTVFBQUFBJCQAAAAAAAAAAAEAAAC-UXTJZ2~S84HMyLsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN0F8lndBfJZdn;"},
    {
        "BDUSS": "Fp6dExzMVNiN0F4N3NXSkhOSkJHQjFpZVBGUkRoTWgtZ3hrLW1uaXdjZmZraGxhTVFBQUFBJCQAAAAAAAAAAAEAAADFUXTJsNfR8rXHusbltAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN8F8lnfBfJZW;"},
    {
        "BDUSS": "ERIS1dPeU9JWXRBeXhJRnE0dGpCUnJmRHJZVkxNRjJwSGxOTVVXeEpBa2hreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABDU3TJyOXRxbXEt-K6zeL5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEG8lkhBvJZe;"},
    {
        "BDUSS": "1d1bGFkZzRsMn44fk5ScU5DVzBBWFg5eS1Yb0xKa1FqR2ZTcDh3WkotVWpreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABNU3TJsdnUxs611q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACMG8lkjBvJZR;"},
    {
        "BDUSS": "UycW1xYWQzdkVrNjhSdUZ4fnFpNEtkREt5a1JURUxlNGZrN0ZseXN1c2hreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABAU3TJuvHcx9HFdGltZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEG8lkhBvJZa2;"},
    {
        "BDUSS": "UJzVDQ3MEFDRnlEQThKNEg2UDQzTG53RW9nRkxvSnVJRjY1TnZZaGw0OXdraGxhSVFBQUFBJCQAAAAAAAAAAAEAAAC~cHTJzOzQq9LCsLLWvgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAF8llwBfJZb;"},
    {
        "BDUSS": "0wVjEwZEdsbDBFRDdwQnVLcmlhanhZUHBiaXlhcHU4aVBCQktrenozQ2lreGxhTVFBQUFBJCQAAAAAAAAAAAEAAACLaXTJwabSucO3ZnJlZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKIG8lmiBvJZeG;"},
    {
        "BDUSS": "m1lWENQcDAzZ0tBRFNhWFdiQnI0VkpyelZYeEhFR0VCTXcwaHJsZ2hHZHFsQmxhTVFBQUFBJCQAAAAAAAAAAAEAAAAFe3TJ6trK6bX7tKvG5gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGoH8llqB~JZc;"},
    {
        "BDUSS": "Ex6Uk9IaFMycWpGOTcyMGgzenpCSTA0V1IzWG9KU3JzY345eXZvTXA3NUtsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAAChlnTJt6rI49TGzOzo0gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEoI8llKCPJZe;"},
    {
        "BDUSS": "NLcHBPUWhjalo0SFFveTR2ZDZXY3JsflhHOURtfmVlNDBLa3pud0xWTDlsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAABe0XTJc2t52a6yycGrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP0I8ln9CPJZR0;"},
    {
        "BDUSS": "V6Q3VGQ3dHVUNwNGQ4eVU2TmF3TXMtQUFONjA3cUVvfllpSWh1SjcxQ0FsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAADGl3TJZmx5w6~EycC8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAI8lmACPJZTl;"},
    {
        "BDUSS": "JraDlsb1cwaVBra3RCaDlFQVN5WE1XTGpxLXJpZG92TmpiLTlRamlCai1sUmxhSVFBQUFBJCQAAAAAAAAAAAEAAADBqHTJs6y8tu~xxO7R4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP4I8ln-CPJZUT;"},
    {
        "BDUSS": "JjTjdnRGhlOHAyTVNIU0w5NFpaRGxielYyZjIzNDFqLU53VElRa35vTH5sUmxhTVFBQUFBJCQAAAAAAAAAAAEAAAB76HTJy-XS1M2utcTAz7OyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8I8ln~CPJZfl;"},
    {
        "BDUSS": "N-NHBDaUcxRlZLTkZlQ09NOHgyQ091YnhEUG9QNEVEc1ZQb1NxR0JHdmNsaGxhTVFBQUFBJCQAAAAAAAAAAAEAAAAo7XTJxKrP47vcZ3JlYXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANwJ8lncCfJZUV;"},
    {
        "BDUSS": "V6czczSVNkRkpkb0NxYkJmY3lnd1dybjRtZHM2YlF5UzF5SWtoYndNcmJsaGxhSVFBQUFBJCQAAAAAAAAAAAEAAAAi7XTJ0v7H7cqrc3VubnkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANsJ8lnbCfJZZ1;"},
    {
        "BDUSS": "NadkpydzZRa0RpLXJPLUN-NnVBU0VJYU9KNnM0QkRveEQ1OGxmTzBKZDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAABty3TJwM3CzLqjbGlmZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYK8ll2CvJZUD;"},
    {
        "BDUSS": "h6MVREU3UzREUtZFl0UHhGNnFYTVhReEJjcUUwcXJ5VX5vSVo0c2VoRDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAACA23TJy6zAyrXEs9nD7ua6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPYK8ln2CvJZY1;"},
    {
        "BDUSS": "2l2RTNnbTNUQjM2MlJwN3lCRlNmSkNzamVRV1BNdkJhamhkek8wcEdhRDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAACC23TJyf7Q49bxZ3JlYXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPYK8ln2CvJZc;"}
]

if __name__ == '__main__':
    for c in cookies:
        print(verification.verify_bduss(c))

    # yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
    # folder_path = os.path.dirname(__file__)
    # file_path  = os.path.join(folder_path,'test.py').replace('\\','/').replace('/','//')
    # yag.send('jonathan@xunlei.net', 'stock_2018-05-23_23-53-53_1527090833.json', self.output_path)

    this_folder = os.path.dirname(__file__)
    parent_folder = os.path.dirname(this_folder)
    output_path = os.path.join(parent_folder, 'output')
    files = os.listdir(output_path)

    stock_files = list(filter(lambda x: 'stock' in x, files))

    newest_stock_file = reduce(lambda a, b: a if int((re.findall('(?<=__).*(?=.json)', a) or ['0'])[0]) >
                                            int((re.findall('(?<=__).*(?=.json)', b) or ['0'])[0]) else b, stock_files)
    print(newest_stock_file)

    # print(reduce(lambda x, y: x if x > y else y, aa))
    # print(os.listdir('..output'))
