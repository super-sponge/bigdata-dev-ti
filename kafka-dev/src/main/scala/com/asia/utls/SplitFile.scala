package com.asia.utls

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by sponge on 2017/2/23 0023.
  */
object SplitFile {
  def main(args:Array[String]): Unit = {

    val SPLITSIZE = 126
    val sparkConf = new SparkConf().setAppName("SplitFile")
    val sc = new SparkContext(sparkConf)
    val textFile = sc.textFile("README.md")
    val size = textFile.map(_.length).sum()
    val count = textFile.count()
    val splitCount = size / SPLITSIZE

    println("Size is " + size)
    println("count is " + count)
    println("splitCount is " + splitCount)

    sc.stop()
    Thread.sleep(1000)

  }

}
