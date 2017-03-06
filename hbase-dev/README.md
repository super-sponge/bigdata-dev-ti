#hbase  测试

## 测试环境登陆
    登陆 10.183.5.31
    在/home/dev 下面建立临时目录
    mkdir liuhb
    测试常用命令请参考 doc/hbase 常用命令

## HBase javaAPI 测试
    根据四川现场 10.183.5.31 /etc/hbase/conf
    export HADOOP_CLASSPATH=`hbase classpath`    
    java -cp $HADOOP_CLASSPATH:./hbase-dev-1.0-SNAPSHOT-jar-with-dependencies.jar HBaseJavaAPI
    
    针对四川现场，表名称写入代码中 private static  final String tableName = "stg:student";
##bulkload
###实例文件
    把下面文件文件内容存入data.txt，其中分隔符为\t。上传data.txt 到hdfs路径
    1001,lilei,17,13800001111
    1002,lily,16,13800001112
    1003,lucy,16,13800001113
    1004,meimei,16,13800001114
    
    hdfs dfs -mkdir /user/dev/input
    hdfs dfs -put data.txt  /user/dev/input
    --查看文件是否上传成功
    hdfs dfs -ls /user/dev/input
    
###hbase 对应的表（bulkload不用创建表)
    hbase shell
    create 'stg:student', {NAME => 'info'}
    
###执行importtsv 导入数据
    Usage: importtsv -Dimporttsv.columns=a,b,c <tablename> <inputdir>
    导入 inputdir 下面的TSV文件到指定表
    HBASE_ROW_KEY 必须指定，代表rowkey
    要使用buldload  需要指定下面参数,如果此参数没有指定,表必须存在
    -Dimporttsv.bulk.output=/path/for/output  （指定此参数后需要调用LoadIncrementalHFiles 导入到hbase)
    
    其他参数
      -Dimporttsv.skip.bad.lines=false - fail if encountering an invalid line
      -Dimporttsv.separator=|' - eg separate on pipes instead of tabs
      -Dimporttsv.timestamp=currentTimeAsLong - use the specified timestamp for the import
      -Dimporttsv.mapper.class=my.Mapper - A user-defined Mapper to use instead of org.apache.hadoop.hbase.mapreduce.TsvImporterMapper
      -Dmapreduce.job.name=jobName - use the specified mapreduce job name for the import
      -Dcreate.table=no - can be used to avoid creation of table by this tool
      Note: if you set this to 'no', then the target table must already exist in HBase
      -Dno.strict=true - ignore column family check in hbase table. Default is false
    
    For performance consider the following options:
      -Dmapreduce.map.speculative=false
      -Dmapreduce.reduce.speculative=false
      
####采用bulk导入数据
    hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.columns=a,b,c -Dimporttsv.bulk.output=hdfs://storefile-outputdir <tablename> <hdfs-data-inputdir>
    hbase org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles <hdfs://storefileoutput> <tablename>
    
    示例
    hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.columns=HBASE_ROW_KEY,info:name,info:age,info:phone -Dimporttsv.separator=, -Dimporttsv.bulk.output=/user/dev/output stg:student /user/dev/input
    hbase org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles /user/dev/output stg:student
    
    hbase shell
    scan 'stg:student'
    清空数据，方便下一步通过api导入数据
    truncate 'stg:student'
    
####采用client api 导入数据
    不指定-Dimporttsv.bulk.output 参数，导入程序默认使用client api直接导入数据
    示例
    hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.columns=HBASE_ROW_KEY,info:name,info:age,info:phone -Dimporttsv.separator=,  ods_ceshi:student /input/ods_ceshi/hbase_bulkdata/in
####hadoop 调用方式（可以不用测试）
    hadoop jar hbase-server-1.2.2.jar importtsv -Dimporttsv.columns=a,b,c -Dimporttsv.bulk.output=hdfs://storefile-outputdir <tablename> <hdfs-data-inputdir>
    hadoop jar hbase-server-1.2.2.jar completebulkload [-c /path/to/hbase/config/hbase-site.xml] <hdfs://storefileoutput> <tablename>
    
###数据验证
    scan 'stg:student', {LIMIT => 10}
    
###编写代码
    借助maven的assembly插件, 生成胖jar包(就是把依赖的zookeeper和hbase jar包都打到该MapReduce包中), 否则的话, 就需要用户静态配置, 在Hadoop的class中添加zookeeper和hbase的配置文件和相关jar包.

## 自定义bulkload
    详细查看HBaseBulkLoad.java
    执行命令
    export HADOOP_CLASSPATH=`hbase classpath`
    hadoop jar sc_hbase-1.0-SNAPSHOT.jar sc.test.HBaseBulkLoad  ods_ceshi:student  /input/ods_ceshi/hbase_bulkdata/in /input/ods_ceshi/hbase_bulkdata/out2
    hbase org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles /input/ods_ceshi/hbase_bulkdata/out2 ods_ceshi:student
## mapreduce 读取文件直接插入hbase
    HBaseMRLoad.java
    实例文件
    sample.csv
    1,info,name,jack
    1,info,score,90
    2,info,name,tom
    2,info,score,85
    
    hbase shell
    create 'stg:sample','info'
    
    hdfs 上传文件
    hdfs dfs -mkdir /user/dev/sample
    hdfs dfs -put sample.csv /user/dev/sample
    打包后上传到服务器
    export HADOOP_CLASSPATH=`hbase classpath`
    hadoop jar hbase-dev-1.0-SNAPSHOT-jar-with-dependencies.jar HBaseMRLoad  /user/dev/sample stg:sample
    
    查看结果:
    hbase shell
    scan 'stg:sample'
    
##  清理数据
    cd /home/dev/liuhb
    rm -rf data.txt
    rm -rf sample.csv
    hdfs dfs -rm -r /user/dev/*
    
    hbase shell
    disable 'stg:sample'
    drop 'stg:sample'
    disable 'stg:student'
    drop 'stg:student'

参考：
    http://blog.csdn.net/lifuxiangcaohui/article/details/41831975