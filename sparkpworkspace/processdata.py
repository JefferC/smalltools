
import json

csvfile = "D:\Profile\PyScript\Pj1\data\\1718hd.csv"
jsofile = "D:\Profile\PyScript\Pj1\data\spark_json.txt"

csvf = open(csvfile,'r')
jsof = open(jsofile,'w')

head = csvf.readline().split(',')

keys = []
js = []

for i in xrange(len(head)):
    if i != 0:
        keys.append(head[i].strip().decode('gbk'))

while True:
    line = csvf.readline()
    if line.strip() == "":
        break
    values = line.decode('gbk').split(',')
    values.pop(0)
    ei = {}
    for e in xrange(len(values)):
        if keys[e].strip() == "":
            continue
        ei[keys[e]] = values[e].strip()
    js.append(ei)

csvf.close()
r = ""
for i in js:
    l = json.dumps(i,ensure_ascii=False)
    r += l + '\n'
jsof.write(r.encode('utf8'))
jsof.close()
