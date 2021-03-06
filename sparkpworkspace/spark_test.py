# encoding: utf8


import json,os,re
import pandas
print os.getenv("HADOOP_HOME")

from pyspark.sql import SparkSession,HiveContext,Row
from pyspark import SparkConf,SparkContext

json_data = r"D:\Profile\PyScript\Pj1\data\spark_json.txt"
parquet_data = r"D:\\Profile\\PyScript\\Pj1\\data\\000000_0"

#conf = SparkConf().appName("first")
#sc = SparkContext(conf=conf)
#hc = HiveContext(sc)


spark = SparkSession.builder.appName("first").getOrCreate()

sc = spark.sparkContext

sc.setLogLevel("ERROR")

hc = HiveContext(sc)


#print spark.__class__

# If the data format is Json, This is simple.(If you dont what to change the columns' name)
def read_josn(svtb=False):
    df = spark.read.json(json_data)
    # select * from global_temp.hardon
    df.createGlobalTempView("hardon")
    # select * from hardon where
    df.createOrReplaceTempView("hardon")
    # Save As table. u shell always format as parquet.so forget about csv,text.
    # mode: overwrite - delete all and create new
    #     : append    - add new file
    #     : error     - throw error if file exists
    #     : ignore    - do nothing if file exists
    if svtb:
        df.write.format('parquet').bucketBy(4,'result').partitionBy("gm").mode("overwrite").saveAsTable("SavedHardon")

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


def PlayWithPandas():
    df = spark.read.json(json_data)
    # The same class
    pd = df.toPandas()
    print pd.__class__
    pd = pandas.DataFrame(data=pd)
    print pd.__class__
    print pd.head()
    print df.head()



#PlayWithPandas()

# below is not good for json. but good for the datafile that did not contains column name
outkeys = []

def ExecJson(l):
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

def ExecFiledsT(p):
    r = Row(ass=p[0],back=p[1],dumps=p[2],faqiu=p[3])
    return r


def SparkSQLWithRDD():
    sc = spark.sparkContext
    lines = sc.textFile(json_data)
    # split fields (JSON)
    parts = lines.map(ExecJson)
    result = parts.map(ExecFiledsT)
    schemaHD = spark.createDataFrame(result)
    schemaHD.createOrReplaceTempView("hardon")
    r = spark.sql("select sum(dumps) from hardon")
    r.show()

#SparkSQLWithRDD()

# ---------------------------------- Spark Python UDF ----------------------------------- #

def SparkFunction(v1,v2):
    v2 = str(v2)
    rex = re.compile(r"^\d+$")
    if not rex.search(v2):
        return None
    r1 = v1[0:int(v2)]
    return r1

def SparkUDF():
    # We need a table, I use hardon. Session: spark
    read_josn()
    #hc.registerFunction("SparkFunction",SparkFunction)
    spark.udf.register("SparkFunction",SparkFunction,'string')
    #rows = spark.sql("select * from hardon")
    rows = spark.sql("select SparkFunction(shot,3),shot from hardon limit 2")
    rows.show()



#SparkUDF()


# --------------------------------- Parquet -------------------------------- #

def OpenParquetFile():
    df2 = spark.read.parquet(parquet_data)
    df2.createOrReplaceTempView('parquet_data')
    spark.sql("select * from parquet_data").show()
    df2.select('id','map1').write.save(r"D:\Profile\spark\\bb",mode='overwrite')
    dirs = os.listdir(r"D:\Profile\spark\\bb")
    for i in dirs:
        if i.split('.')[-1] == 'parquet':
            df3 = spark.read.parquet("D:\Profile\spark\\bb\\%s" %i)
            df3.show()
            break


#OpenParquetFile()


# ------------------------------- SaveAsTable ------------------------------ #

def SaveAsHiveTable():
    # So we need a table too....
    read_josn(True)

#SaveAsHiveTable()

# ------------------------------- Read -------------------------------- #

def ReadParquet():
    p = r"D:\Profile\PyScript\Pj1\sparkpworkspace\spark-warehouse\savedhardon"
    p = r"D:\Profile\cp\savedhardon_linux"
    # Very Low
    '''
    for absd,nouse,listdir in os.walk(p):
        for i in listdir:
            if i.split('.')[-1] == 'parquet':
                i = absd + os.sep + i
                print i
                df3 = spark.sql("select * from parquet.`%s`" %i)
                df3.show()
    '''
    # look here
    beautiful = spark.read.option('mergeSchema','true').parquet(p)
    #beautiful.printSchema()
    beautiful.show()


ReadParquet()




spark.stop()