# coding:utf8

# Author: Cai, Jiefei
# Date  : 2018/11/22

import Config
import urllib2
import time


def get_url():
    urls = []
    for i in Config._StockList:
        urls_tmp = map(lambda x:Config.market+x, i)
        url = ','.join(urls_tmp)
        url = Config.url + url
        urls.append(url)
    return urls


def get_result(url):
    request = urllib2.Request(url)
    # request.add_header('Accept-Encoding', 'gzip, deflate')
    # request.add_header('Accept-Language', 'zh-CN,zh;q=0.9')
    # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36')
    resp = urllib2.urlopen(request)
    r = resp.readlines()
    resp.close()
    return r


def main():
    urls = get_url()
    for i in urls:
        q = get_result(i)
        for j in q:
            #print j.decode('gb2312').strip()
            print j.strip()
        time.sleep(10)


def run():
    if True:
        main()
        time.sleep(3000)


if __name__ == '__main__':
    run()