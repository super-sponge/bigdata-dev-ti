import org.apache.hadoop.mapred.lib.MultipleTextOutputFormat

import org.apache.spark._
import org.apache.spark.SparkContext._

/**
  * Created by sponge on 2017/2/23 0023.
  */


class RDDMultipleTextOutputFormat extends MultipleTextOutputFormat[Any, Any] {
  override def generateFileNameForKeyValue(key: Any, value: Any, name: String): String = key.asInstanceOf[String]
}

object Split {
  val SPLITSIZE = 1024
  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("Split")
    val sc = new SparkContext(conf)

    val textFile = sc.textFile("/tmp/README.md")
    val size = textFile.map(_.length).sum()
    val count = textFile.count()
    val splitCount = (size / SPLITSIZE).toInt
    val accum = sc.accumulator(0, "Example Accumulator")


    textFile.map(x => ((accum.value % splitCount).toString, x)).partitionBy(new HashPartitioner(splitCount)).saveAsHadoopFile("/tmp/example", classOf[String], classOf[String],classOf[RDDMultipleTextOutputFormat])



//    sc.parallelize(List(("w", "www"), ("b", "blog"), ("c", "com"), ("w", "bt")))
//      .map(value => (value._1, value._2 + "Test"))
//      .partitionBy(new HashPartitioner(3))
//      .saveAsHadoopFile("/tmp/iteblog", classOf[String], classOf[String],classOf[RDDMultipleTextOutputFormat])

    sc.stop()

  }
}
