cat ./start-stream.sh



for file in ./lib/*jar
do
jars=$file,$jars
done

jars=${jars}spark-dev-1.0-SNAPSHOT.jar
echo $jars


export spark_res="--num-executors 4 --driver-memory 512m --executor-memory 512m --executor-cores 4"
export SPARK_MAJOR_VERSION=1

spark-shell --master yarnclient --class stream.FlumeEventCount ${spark_res} --jars ${jars} fileintf01 9999

http://spark.apache.org/docs/1.6.1/streaming-flume-integration.html