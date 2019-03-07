# coding: utf-8

# Author: Cai, Jiefei
# Date  : 2018/08/03 10:23:00

import Config
import os, re, sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



def getchild(e,l=[]):
    if e.getchildren() == []:
        if e.text is not None and e.text.strip() not in ["", 'none']:
            l.append([e.tag, e.text])
    else:
        for i in e.getchildren():
            # 循环获取子xml
            getchild(i, l)
    return l

'''
    search_sub是启用正则的查找方式
    参数说明：
    p：文件路径
    reg：正则表达式字符串
    Controls：从哪些控件里找
    sctp：ktr或者kjb分别对应trans或者job
'''
def search_sub(p, reg, Controls, sctp='ktr'):
    try:
        r = re.compile(reg)
    except Exception as e:
        print "regexp error\n%s" %str(e)
        exit(12)
    #f = open(p)
    # 小写
    #f1 = f.read().lower()
    #f.close()
    # 有bug
    #if not r.search(f1):
    #    return 0
    try:
        t = ET.ElementTree(file=p.decode("gbk"))
    except:
        return 0
    if sctp == 'ktr':
        steps = t.findall("step")
    else:
        steps_tmp = t.findall("entries")
        steps = steps_tmp[0].findall("entry")
    rt = {}
    for i in steps:
        ls = getchild(i, [])
        tp = {"value": ls,
              "type": i.find("type").text}
        rt[i.find("name").text] = tp
    for st in rt:
        for i in rt[st]["value"]:
            if 'all' not in Controls:
                if rt[st]['type'].lower() in Controls:
                    if r.search(i[1].lower()):
                        resu = p + "\t" + st + "\t" + i[1].replace("\n"," ").replace("\r"," ").replace("\t"," ")
                        print resu.encode('utf8')
            else:
                #print i[1].lower()
                if r.search(i[1].lower()):
                    resu = p + "\t" + st + "\t" + i[1].replace("\n"," ").replace("\r"," ").replace("\t"," ")
                    print resu.encode('utf8')

'''
    search_sub_no_reg是不启用正则的查找方式
    参数说明：
    p：文件路径
    reg：查找字符串
    Controls：从哪些控件里找
    sctp：ktr或者kjb分别对应trans或者job
'''
def search_sub_no_reg(p, reg, Controls, sctp='ktr'):
    f = open(p)
    # 全小写了
    f1 = f.read().lower()
    f.close()
    if reg not in f1:
        return 0
    try:
        # Gbk编码打开
        t = ET.ElementTree(file=p.decode("gbk"))
    except:
        return 0
    if sctp == 'ktr':
        steps = t.findall("step")
    else:
        steps_tmp = t.findall("entries")
        steps = steps_tmp[0].findall("entry")
    rt = {}
    for i in steps:
        ls = getchild(i, [])
        tp = {"value": ls,
              "type": i.find("type").text}
        rt[i.find("name").text] = tp
    for st in rt:
        for i in rt[st]["value"]:
            if 'all' not in Controls:
                if rt[st]['type'].lower() in Controls:
                    if reg in i[1].lower():
                        resu = p + "\t" + st + "\t" + i[1].replace("\n"," ").replace("\r"," ").replace("\t"," ")
                        # 这里根据实际情况修改。有些终端默认是gbk的如果用utf打印可能报错或者乱码
                        print resu.encode('utf8')
            else:
                if reg in i[1].lower():
                    resu = p + "\t" + st + "\t" + i[1].replace("\n"," ").replace("\r"," ").replace("\t"," ")
                    # 这里根据实际情况修改。有些终端默认是gbk的如果用utf打印可能报错或者乱码
                    print resu.encode('utf8')


def returnfile(p, sctp='ktr'):
    l = []
    for d, d2, f in os.walk(p, True):
        for i in f:
            if i.split(".")[-1] == sctp:
                l.append(d+os.sep+i)
    return l


def search(s,ifReg=True,sctp='ktr'):
    if not isinstance(s,str):
        return False
    # 搜索路径为空则搜索全目录
    if Config.path == "":
        path = Config.kettle_dir
    else:
        path = Config.kettle_dir + Config.path
    files = returnfile(path, sctp)
    print "file name\tcontrol name\tText"
    Controls = map(lambda x: x.lower(), Config.Controls)
    if ifReg:
        for f in files:
            search_sub(f, s, Controls, sctp)
    else:
        for f in files:
            search_sub_no_reg(f, s, Controls, sctp)


def main():
    if len(sys.argv) >= 2:
        # 如果是参数来的，小写一下。可改
        s = sys.argv[1].lower()
        if len(sys.argv) >= 3:
            if sys.argv[2] == '1':
                ifReg = True
            else:
                ifReg = False
        else:
            ifReg = Config.regexp
        # 判断搜索文件类型，第三个参数
        if len(sys.argv) >= 4:
            sctp = sys.argv[3]
        else:
            sctp = Config.SourchFileType
    else:
        s = Config.searchstring
        ifReg = Config.regexp
        sctp = Config.SourchFileType
    # 考虑到多个字符串一起查的情况
    if isinstance(s, list):
        for i in s:
            search(i, ifReg=ifReg, sctp=sctp)
            if sctp == 'kjb':
                search(i, ifReg=ifReg, sctp='ktr')
    else:
        search(s, ifReg=ifReg, sctp=sctp)
        if sctp == 'kjb':
            search(s, ifReg=ifReg, sctp='ktr')
    return True


if __name__ == "__main__":
    main()
