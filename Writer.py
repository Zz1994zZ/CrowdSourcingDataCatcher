#coding:utf8
import  pymysql
import traceback
from DBUtils.PooledDB import PooledDB
class Writer:
    def __init__(self):
        self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='', db='crowdSourcing',charset="utf8", port=3306)
        # self.conn = pymysql.connect(
        #     host='localhost',
        #     port=3306,
        #     user='root',
        #     passwd='',
        #     db='crowdSourcing',
        #     charset="utf8"
        # )
    def getUserList(self):
        sql='SELECT id from user'
        conn = self.pool.connection()
        cur = conn.cursor()
        try:
            # 执行sql语句
            list=cur.execute(sql)
            list=cur.fetchall()
            # 提交到数据库执行
        except:
            traceback.print_exc()
        cur.close()
        conn.close()
        return list
    def save(self,user):
        if(user==None):
            return
        conn=self.pool.connection()
        cur =conn .cursor()
        try:
            # 执行sql语句
            cur.execute("INSERT INTO `user` VALUES ('" +
                        user.id + "', '" +
                        user.nickname + "', '" +
                        user.city + "', '" +
                        user.work + "', '" +
                        user.price + "', '" +
                        user.workPlace + "', '" +
                        user.workTime + "', \"" +
                        str(user.skillList)+ "\");")
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()
            traceback.print_exc()
        cur.close()
        conn.close()
    def updateSkills(self,user):
        if(user==None):
            return
        conn=self.pool.connection()
        cur =conn .cursor()
        try:
            # 执行sql语句
            cur.execute("update user set skillList= \"" +
                        str(user.skillList)+ "\" where id ="+user.id)
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()
            traceback.print_exc()
        cur.close()
        conn.close()