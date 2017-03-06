#encoding:utf-8

"""
程序名称：切割文件
程序功能：切割文件夹下文件
开发者： 刘红波
开发日期：2017-02-24

"""


from lib.comm import init,printRunInfo
from lib.comm import logger


import getopt,sys,optparse
from pyspark import SparkConf,SparkContext

import sys
import time
def usage():
    print "error "
def getOpts(argv):
    try:
        options,args = getopt.getopt(argv[1:],"hi:o:n:",["help","in=","out=","num="])
        for name,value in options:
            if not name:
                usage()
            if  name in ("-h","--help"):
                usage()
            if name in ("-i","--in"):
                v_in = value
            if name in ("-o","--out"):
                v_out = value
            if name in ("-n","--num"):
                n_num = value
        return (v_in, v_out, n_num)
    except getopt.GetoptError:
        sys.exit()

if __name__=='__main__':
    # 此处需要更新为自己的程序名(程序名就是表名),
    v_app_name = 'utils_split_file'
    (v_in, v_out, v_num) = getOpts(sys.argv)
    init(v_app_name, '')
    logger.info(v_app_name + ' 开始运行...')

    logger.info(u'输入文件路径: ' + v_in)
    logger.info(u'输出文件路径: ' + v_out)
    logger.info(u'分割数量: ' + v_num)

    try:
        logger.info(u'spark环境初始化...')
        conf = SparkConf().setAppName(v_app_name)
        sc = SparkContext(conf = conf)
        v_begin = time.time()

        sc.textFile(v_in).repartition(int(v_num)).saveAsTextFile(v_out)

        sc.stop()
        #程序结束打印结束信息
        v_end = time.time()
        logger.info("[%s] 输入目录:%s 输出目录:%s 分割数量:%s 开始时间:%s 结束时间: %s 共耗时 %ds"%(
            v_app_name,
            v_in,
            v_out,
            v_num,
            time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_begin)),
            time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(v_end)),
            v_end - v_begin))


    except (KeyboardInterrupt, EOFError):
        logger.error("\nAborting ... Keyboard Interrupt.")
        sys.exit(1)

