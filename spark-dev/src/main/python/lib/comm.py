#encoding:utf-8

import logging
import logging.handlers
import logging.config
import getopt,sys,optparse

import time,datetime


logger = logging.getLogger()



def setup_logging(logger, filename, logging_level):
    formatstr = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d - %(message)s"
    formatstr = "%(levelname)s %(asctime)s - %(message)s"
    formatter = logging.Formatter(formatstr)
    rotateLog = logging.handlers.RotatingFileHandler(filename, "a", 10000000, 25)
    rotateLog.setFormatter(formatter)
    logger.addHandler(rotateLog)

    logging.basicConfig(format=formatstr, level=logging_level, filename=filename)
    logger.setLevel(logging_level)

    console = logging.StreamHandler()
    console.setLevel(logging_level)
    console.setFormatter(formatter)
    logger.addHandler(console)
    #
    # logger.info("loglevel=logging.{0}".format(logging._levelNames[logging_level]))

def init(app_name, v_data_f):
    # setup_logging(logger, '/home/ods_ceshi/app/odsprg/logs/' + app_name + '_' + v_data_f + '.log', logging.INFO)
    setup_logging(logger, 'd:/tmp/logs/' + app_name + '_' + v_data_f + '.log', logging.INFO)

def getOpts(argv):
    try:
        options,args = getopt.getopt(argv[1:],"hd:l:",["help","date=","latn_id="])
        for name,value in options:
            if not name:
                usage()
            if  name in ("-h","--help"):
                usage()
            if name in ("-d","--date"):
                v_date = value
            if name in ("-l","--latn_id"):
                v_latn = value
        return (v_date, v_latn)
    except getopt.GetoptError:
        usage()
        sys.exit()

def printRunInfo(logger, v_app_name, v_date, v_latn, v_begin, v_end):
    import time
    logger.info("[%s] 抽取账期:%s 抽取地市:%s 开始时间:%s 结束时间: %s 共耗时 %ds"%(
        v_app_name,
        v_date,
        v_latn,
        time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_begin)),
        time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_end)),
        v_end - v_begin))

def getDate(v_date, delta, iformat = "%Y-%m-%d", oformat = "%Y-%m-%d"):
    d1 = datetime.datetime.strptime(v_date,iformat)
    d3 = d1 + datetime.timedelta(days = delta)
    if iformat != "%Y-%m-%d" and oformat == "%Y-%m-%d":
        return d3.strftime(iformat)
    else:
        return d3.strftime(oformat)
def getTableStoreType():
    return "parquet"

def usage():
    logger.info(u"""
    -h / --help :使用帮助
    -d / --date : 输入账期
    -l / --latn_id :输入地市
    """)

if __name__ == '__main__':
    print(getDate('2017-02-14', -1))
    print(getDate('2017-02-14', 1))
    print(getDate('2017-02-14', 2))
    print(getDate('20170214', 2, "%Y%m%d"))
    print(getDate('20170214', 0, "%Y%m%d", "%Y%m"))
    print(getDate('2017-02-14', 0, oformat='%Y%m' ))
    print(getDate('2017-02-14', 0))