# coding: utf-8

import re,xlrd


def replaceit(doc):
    doc2 = doc.split('\n')
    doc = []
    for i in doc2:
        if i not in doc:
            doc.append(i)
    
    r = re.compile(r"(^\w|_\w)")
    result_a = []
    for i in doc:
        i_bak = i
        i = i.strip()
        if i == i.upper():
            i = i.lower()
        j = r.sub(matchit,i)
        result = []
        result.append(i_bak)
        result.append(j)
        if j != i_bak:
            result.append(1)
        else:
            result.append(0)
        result_a.append(result)
    return result_a

def matchit(matched):
    s = matched.group(0)
    s = s.upper()
    return s



def UpCase():
    a = open(r"D:\\Profile\\cp\\tbfile.txt",'r')
    b = a.read()
    a.close()
    res = replaceit(b)
    for i in res:
        if i[2] == 1:
            st = "1\t" + i[1] + "\tALTER TABLE guba.%s RENAME TO guba.%s;" %(i[0],i[1]+"_Bak_Mid")
            st = st + "\tALTER TABLE guba.%s RENAME TO guba.%s;" %(i[1]+"_Bak_Mid",i[1])
        else:
            st = "0\t" + i[1]
        print st

def AddPrimaryKey(di):
    book = xlrd.open_workbook(di)
    shcol = book.sheet_by_index(1)
    # 拿出所有需要更新的
    Modify = {}
    for i in xrange(shcol.nrows):
        if i == 0:
            continue
        if shcol.row(i)[4].value == 0 or shcol.row(i)[4].value == '':
            continue
        if shcol.row(i)[3].value == 0 or shcol.row(i)[3].value == '':
            continue
        tablename = shcol.row(i)[0].value.strip()
        colname = shcol.row(i)[1].value.strip()
        if tablename not in Modify:
            Modify[tablename] = []
        Modify[tablename].append(colname)
    # 拿出所有已经有主键的
    Already = {}
    for i in xrange(shcol.nrows):
        if i == 0: continue
        if shcol.row(i)[5].value in [0,'']: continue
        tablename = shcol.row(i)[0].value.strip()
        colname = shcol.row(i)[1].value.strip()
        if tablename not in Already:
            Already[tablename] = []
        Already[tablename].append(colname)
    # 整理出要删的
    AlreadyKey = Already.keys()
    for i in AlreadyKey:
        if i not in Modify:
            Already.pop(i)
    # 删除已经存在的主键
    for i in Already:
        print "ALTER TABLE guba.%s DROP CONSTRAINT C_PRIMARY;" %i
    # 添加主键
    for i in Modify:
        tag = ','.join(Modify[i])
        print "alter table guba.%s add primary key(%s)" %(i,tag)
    return Modify,Already




if __name__ == '__main__':
    #UpCase()
    r1,r2 = AddPrimaryKey(r"D:\\Profile\\cp\\gb.xlsx")

    
