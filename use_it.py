import re


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
            st = "1\t" + i[1] + "\tALTER TABLE guba.%s RENAME TO guba.%s;" %(i[0],i[1])
        else:
            st = "0\t" + i[1]
        print st

def ReNameTb():
    



if __name__ == '__main__':
    UpCase()
    
    
