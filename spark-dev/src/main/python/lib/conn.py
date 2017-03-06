#encoding:utf-8

from pyspark import SparkConf,SparkContext
from pyspark.sql import HiveContext


class Conn():
    """
    封装spark 连接
    """
    def __init__(self, name, db = 'ods_ceshi'):
        self.name = name
        conf = SparkConf().setAppName(name)
        self.sc = SparkContext(conf = conf)
        self.hc = HiveContext(self.sc)
        self.hc.sql("use " + db)
        self.hc.registerFunction("identify", identify)

    def _exec_query(self, v_sql, logger, desc=''):
        import time
        try:
            if desc != '':
                logger.info(desc)

            v_begin = time.time()
            result = self.hc.sql(v_sql)
            v_end = time.time()
            logger.info("[%s]开始时间:%s 结束时间: %s 共耗时 %ds sql语句 [ %s ]"%(
                self.name,
                time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_begin)),
                time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_end)),
                v_end - v_begin,
                v_sql
            ))
            return  result
        except:
            logger.error("[%s]错误语句: %s" %(self.name, v_sql))
            raise Exception('Error raise')
    def exec_query(self, v_sql, logger, desc=''):
        step = 1
        for sql in v_sql.split(";"):
            self._exec_query(sql, logger, desc + "step_" + str(step))
            step = step + 1

def identify(text):
    return "1"

if __name__ == "__main__":
    try:
        conn = Conn('conn')
    except (KeyboardInterrupt, EOFError):
        print("\nAborting ... Keyboard Interrupt.")
        sys.exit(1)
