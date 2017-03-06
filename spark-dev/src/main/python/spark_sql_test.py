#encoding:utf-8

"""
程序名称：程序测试
程序功能：测试程序功能
开发者：  刘红波
开发日期：2017-02-28

spark-sql --master yarn-client --principal ods_ceshi@AI.COM --keytab  /tmp/hive.service.keytab

hdfs dfs -put kv1.txt  /user/ods_ceshi

spark-submit --master yarn-client --principal ods_ceshi --keytab /tmp/hive.service.keytab  spark_sql_test.py
"""

from pyspark import SparkConf,SparkContext
from pyspark.sql import HiveContext


def main():
    conf = SparkConf().setAppName('spark_sql_test')
    sc = SparkContext(conf = conf)
    sqlContext = HiveContext(sc)

    sqlContext.sql("use default")
    sqlContext.sql("create table if not exists testtab(id int , name string)")
    sqlContext.sql("LOAD DATA INPATH '/user/ods_ceshi/kv1.txt' INTO TABLE testtab")
    sqlContext.sql("create table if not exists testtabnum(id int , num int)")
    sqlContext.sql("insert into table testtabnum select id, count(*) from testtab group by id")

    sc.stop()

if __name__ == '__main__':
    main()
