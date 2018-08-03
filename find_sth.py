# coding: utf-8

# Author: Cai, Jiefei
# Date  : 2018/08/03 10:23:00

import Config
import os,re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



def getchild(e,l=[]):
    if e.getchildren() == [] and e.text is not None and e.text.strip() not in ["",'none']:
        l.append([e.tag,e.text])
    else:
        for i in e.getchildren():
            getchild(i,l)
    return l


def search_sub(p,reg):
    try:
        r = re.compile(reg)
    except:
        print "regexp error"
        exit(12)
    f = open(p)
    f1 = f.read().lower()
    f.close()
    if not r.search(f1):
        return 0
    try:
        t = ET.ElementTree(file=p.decode("gbk"))
    except:
        return 0
    steps = t.findall("step")
    rt = {}
    for i in steps:
        ls = getchild(i, [])
        tp = {"value": ls,
              "type": i.find("type").text}
        rt[i.find("name").text] = tp
    for st in rt:
        for i in rt[st]["value"]:
            if r.search(i[1].lower()):
                print p + "\t" + st + "\t" + i[1].replace("\n"," ")

def returnfile(p):
    l = []
    for d,d2,f in os.walk(p,True):
        for i in f:
            if i.split(".")[-1] == 'ktr':
                l.append(d+os.sep+i)
    return l

def search(s):
    if not isinstance(s,str):
        return False
    # 搜索路径为空则搜索全目录
    if Config.path == "":
        path = Config.kettle_dir
    else:
        path = Config.kettle_dir + Config.path
    files = returnfile(path)
    print "file name\tcontrol name\tText"
    for f in files:
        search_sub(f,Config.searchstring)

def main():
    if isinstance(Config.searchstring,list):
        for i in Config.searchstring:
            search(i)
    else:
        search(Config.searchstring)
    return True



if __name__ == "__main__":
    main()
