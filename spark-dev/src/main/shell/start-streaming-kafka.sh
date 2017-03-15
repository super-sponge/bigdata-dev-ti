#!/usr/bin/env bash


base_dir=$(dirname $0)/..




jars=$base_dir/spark-dev-1.0-SNAPSHOT.jar
for jar in ${base_dir}/lib/*jar
do
jars=$jars,$jar
done

echo "$jars"
export spark_res="--num-executors 2 --driver-memory 512m --executor-memory 512m --executor-cores 1"
export SPARK_MAJOR_VERSION=1

classname=stream.KafkaWordCount
sparkname=kafkawordcount
runjar=$base_dir/spark-dev-1.0-SNAPSHOT.jar
argvs="localhost:2181 group1 topic1,topic2,topic3 4"
spark-submit --class $classname --name $sparkname --jars $jars $runjar $argvs
