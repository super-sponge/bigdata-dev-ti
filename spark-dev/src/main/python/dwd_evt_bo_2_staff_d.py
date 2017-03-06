#encoding:utf-8

"""
程序名称：程序测试
程序功能：测试程序功能
开发者：  刘红波
开发日期：2017-02-28

spark-sql --master yarn-client --principal ods_ceshi@AI.COM --keytab  /tmp/hive.service.keytab

hdfs dfs -put kv1.txt  /user/ods_ceshi
"""


from lib.comm import init,getOpts,printRunInfo,getTableStoreType
from lib.comm import logger
from lib.conn import Conn


import sys
import time


if __name__=='__main__':
    # 此处需要更新为自己的程序名(程序名就是表名),
    v_app_name = 'dwd_evt_bo_2_staff_d'
    (v_date, v_latn) = getOpts(sys.argv)
    v_date_ft = v_date.replace('-','')
    v_month	= v_date_ft[0:6]
    init(v_app_name, v_date_ft)
    logger.info(v_app_name + ' 开始运行...')
    logger.info(u'输入账期: ' + v_date)
    logger.info(u'输入地市: ' + v_latn)

    try:
        logger.info(u'spark环境初始化...')
        conn = Conn(v_app_name, 'stg')
        v_begin = time.time()

        v_sql = """drop table if exists testtab;
                  create table if not exists testtab(id int , name string)
                  """
        #执行建表sql语句
        conn.exec_query(v_sql,logger,u'执行建表sql语句')

        #执行插入语句
        v_sql= """
        LOAD DATA INPATH '/user/stg/kv1.txt' INTO TABLE testtab
        """
        conn.exec_query(v_sql, logger, u'执行插入语句')

        #执行语句并查询
        v_sql = """
        create table if not exists testtabnum(id int , num int);
        insert into table testtabnum
        select id, count(*) from testtab group by id
        """
        conn.exec_query(v_sql, logger, u'执行插入语句,并计算')

        #清理表
        v_sql = """
            drop table if exists testtab;
            drop table if exists testtabnum
        """
        # conn.exec_query(v_sql, logger, u"清理表")

        #程序结束打印结束信息
        v_end = time.time()
        printRunInfo(logger, v_app_name, v_date, v_latn, v_begin, v_end)

    except (KeyboardInterrupt, EOFError):
        logger.error("\nAborting ... Keyboard Interrupt.")
        sys.exit(1)























































