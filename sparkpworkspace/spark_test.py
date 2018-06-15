
import json
from pyspark.sql import SparkSession
from pyspark.sql import Row

json_data = r"D:\Profile\PyScript\Pj1\data\spark_json.txt"

spark = SparkSession.builder.appName("first").getOrCreate()

# Test read
def read_josn():
    df = spark.read.json(json_data)
    # select * from global_temp.hardon
    #df.createGlobalTempView("hardon")
    # select * from hardon where
    df.createOrReplaceTempView("hardon")

def LetsPlayThisGame():
    read_josn()
    while True:
        a = raw_input("sql:")
        try:
            #b = spark.sql(a.decode('gbk').encode('utf8'))
            b = spark.sql(a)
            b.show()
        except Exception as e:
            print e
            continue

outkeys = []

def ExecJson():
    js = json.loads(l)
    keys = js.keys()
    keys.sort()
    outkeys = keys
    r = []
    for i in keys:
        r.append(js[i])
    return r

def ExecFileds():
    r = Row(set(outkeys))
    # ToDo
    # Can't find out how to use Row function in Auto mode.
    # It seems that i must input every columns and the values.

def SparkSQLWithRDD():
    sc = spark.sparkContext
    lines = sc.textFile(json_data)
    # split fields (JSON)
    parts = lines.map(ExecJson)
    result = parts.map()

SparkSQLWithRDD()