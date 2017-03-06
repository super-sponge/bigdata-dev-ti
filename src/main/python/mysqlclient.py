#!/usr/bin/python
#coding:utf8

"""
create table py_step(
  id bigint(20) not null auto_increment comment '主键',
  node_name     text comment '程序名称,必须与前台流程配置一致',
 step_id       int comment 'stepId',
 step_desc	   text comment 'step描述',
 step_sql      text comment '执行的sql语句',
 start_time    timestamp comment '开始时间',
 end_time      timestamp comment '结束时间',
 state         int default '0' comment '成功标记: 0->成功, 1->失败',
 run_log	     text comment '运行日志',
  primary key (id)
 );

 日志表建立语句


"""
import MySQLdb

config = {
    'host': 'xj1',
    'port': 3306,
    'user': 'user1',
    'passwd': 'user1',
    'db': 'testdb',
    'charset': 'utf8'
}


class MysqlClient():
    """
    封装mysql client 连接
    """

    def __init__(self, config):
        self.db = MySQLdb.connect(**config)
        self.cursor = self.db.cursor()
    def __del__(self):
        self.db.close()

    def executeSQL(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except:
            # 发生错误时回滚
            self.db.rollback()
            return False
    def insertRow(self, nodeName, stepId, stepDesc, stepSql, startTime, endTime, State, runLog):
        v_sql = """insert into py_step(node_name,step_id,step_desc,step_sql,start_time,end_time,state,run_log)
        values ('%s', %d, '%s','%s','%s','%s', '%d', '%s')
        """%(nodeName, stepId, stepDesc, stepSql, startTime, endTime, State, runLog)
        self.executeSQL(v_sql)

    def printVersion(self):
        self.cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取一条数据库。
        data = self.cursor.fetchone()
        print "Database version : %s " % data


if __name__ == '__main__':
    # create database testdb;
    # grant all privileges on testdb.* to 'user1'@'%' identified by 'user1';
    # testConnect(config)
    mysqlClient = MysqlClient(config)
    mysqlClient.printVersion()
    mysqlClient.insertRow("node_name",
                          1,
                          "this is a describe",
                          "insert into table select * from tb1",
                          "2017-02-24 13:02:14",
                          "2017-02-24 14:32:12",
                          0,
                          "this is a runlog")

