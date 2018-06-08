
import os,re

sqldir = r"data\aaa.ddl"

PRINT_COL_TYPE = True
RETURN_SELECT = True
INITIALIZE_DDL = True


def get_col(sqldir):
    if not os.path.isfile(sqldir):
        print "Cant Find File %s" %sqldir
        return False
    try:
        fi = open(sqldir,'r')
        f = fi.read()
        r1 = re.compile(r"[\s\S]*?\(([\s\S]+)\)")
        r2 = re.compile(r"(?<=[^\d\s*]),[\s|\n]*")
        q1 = r1.findall(f.strip())
        q2 = r2.split(q1[0])
        w = []
        for i in q2:
            w.append(i.strip())
        if w == []: exit(1)
        r3 = re.compile(r"(?<=[^\d|^\s])\s+")
        r4 = re.compile(r"\s+")
        col = []
        tp = []
        other = []
        for i in w:
            j = r3.split(i)
            col.append(j.pop(0))
            tp.append(r4.sub("",j.pop(0)))
            other.append(' '.join(j))
        return col,tp,other
    finally:
        if 'fi' in vars():
            fi.close()

def get_Table_Name(sqldir):
    if not os.path.isfile(sqldir):
        print "Cant Find File %s" %sqldir
        return False
    try:
        fi = open(sqldir,'r')
        f = fi.read().lower()
        r1 = re.compile(r"create[\s\S]+table\s+(.*)\s+")
        tb = r1.findall(f)
        if len(tb)>0:
            return tb[0]
        else:
            return False
    finally:
        if 'fi' in vars():
            fi.close()



def Print_Col(sqldir):
    c,t,o = get_col(sqldir)
    nm = get_Table_Name(sqldir)
    if nm:
        print nm.upper()
    for i in xrange(len(c)):
        print c[i]+'\t'+t[i]

def Return_select(sqldir):
    c,t,o = get_col(sqldir)
    nm = get_Table_Name(sqldir)
    if nm:
        nm = nm.upper()
    sql = "SELECT "
    for i in xrange(len(c)):
        if i != 0:
            sql += '\t,'
        sql += c[i]
        sql += "\n"
    sql += " FROM %s" %nm
    print sql

def Initialize_Ddl(sqldir):
    c,t,o = get_col(sqldir)
    nm = get_Table_Name(sqldir)
    if nm:
        nm = nm.upper()
    sql = 'CREATE TABLE %s\n(\n' %nm
    for i in xrange(len(c)):
        sql += '\t%s %s' %(c[i],t[i])
        if o[i].strip() != '':
            sql += o[i]
        if i+1 != len(c):
            sql += ',\n'
    sql += "\n);"
    print sql



if __name__ == '__main__':
    if PRINT_COL_TYPE:
        Print_Col(sqldir)
        print '\n'
    if RETURN_SELECT:
        Return_select(sqldir)
        print '\n'
    if INITIALIZE_DDL:
        Initialize_Ddl(sqldir)
