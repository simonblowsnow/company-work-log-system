#coding:utf8

import sys
sys.path.append("..")


from src.config import Mysql as cfg
import mysql.connector
from DBUtils.PooledDB import PooledDB
from src.libs.log import L



class Database(object):
    ''' For query data in only one code '''
    initFlag = False
    objCount = 0
    pool = None
   
    def __init__(self):
        self.objIndex = Database.objCount
        Database.objCount += 1
        self.lsConn = []
        self.lsCurs = []
        
    def getConnection(self):
        '''检查是否初始化'''
        if not Database.pool:
            Database.pool = PooledDB(mysql.connector, cfg.POOL_SIZE, host=cfg.HOST, port=cfg.PORT, 
                    user=cfg.USER_NAME, passwd=cfg.PASSWORD, db=cfg.DB_NAME, use_unicode=True, charset='utf8')
        cnx = None
        try:
            cnx = Database.pool.connection()
            self.lsConn.append(cnx)
        except:
            L.error('pool error:' + str(len(self.lsConn)))
        return cnx
    
    def selectLine(self, sql, params):
        res = self.selectEx(sql, params)
        if not res or len(res) == 0: return None
        return res[0]
    
    def selectEx(self, sql, params, cursor=None):
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
        cursor.execute(sql, params)
        dt = cursor.fetchall()
        cursor.close()
        cnx.close()
        
        return dt

    def read_all(self, sql, params=None, cursor=None):
        cnx = self.getConnection()
        if cursor == None:
            cursor = cnx.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
        cursor.execute(sql, params)
        dt = cursor.fetchall()
        cursor.close()
        cnx.close()

        return dt

    def read_one(self, sql, params=None, cursor=None):
        cnx = self.getConnection()
        if cursor == None:
            cursor = cnx.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
        cursor.execute(sql, params)
        dt = cursor.fetchone()
        cursor.close()
        cnx.close()

        return dt

    def read_value(self, sql, params=None, cursor=None):
        cnx = self.getConnection()
        if cursor == None:
            cursor = cnx.cursor()
        cursor.execute(sql, params)
        dt = cursor.fetchone()
        cursor.close()
        cnx.close()

        return dt[0]

    def select(self, sql, params, cursor = None):
        # self.checkConnection()
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        
        cursor.execute(sql, params)
        
        return cursor
    
    def selectData(self, sql, params, one=True):
        return self._selectDataAll(sql, params, one)
    
    def _selectDataAll(self, sql, params, one=True):
        cnx = self.getConnection()
        cursor = cnx.cursor(dictionary=True)
        self.lsCurs.append(cursor)
        
        cursor.execute(sql, params)
        dt = cursor.fetchone() if one else cursor.fetchall()
        cursor.close()
        return dt
    
    def selectPage(self, sql, params, page, size, cursor = None):
        sqlEx = "select count(*) from (" + sql + ") sc"
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        cursor.execute(sqlEx, params)
        res = cursor.fetchall()
        
        sql += " limit %s, %s"
        args = list(params) + [int(page) * int(size), int(size)]
        cursor.execute(sql, tuple(args))
        # print sql, page * size, size
        
        return res[0][0], cursor

    def selectPageExt(self, sql, params, page, size, cursor=None):
        sqlEx = "select count(*) from (" + sql + ") sc"
        count = self.read_value(sqlEx,params)
        sql += " limit %s, %s"
        args = list(params) + [int(page) * int(size), int(size)]
        data = self.read_all(sql,params=args)
        return count, data
    
    def execute(self, sql, params):
        cnx = self.getConnection()
        cursor = cnx.cursor()
        
        emp_no = 0
        try:
            cursor.execute(sql, params)
            emp_no = cursor.lastrowid
            cnx.commit()
        except Exception as e:
            emp_no = -1
            print("Run Error: ", sql)
            print(str(e))
        '''End Try'''    
        cursor.close()
        cnx.close()
        return emp_no
    
    def run(self, sql):
        cnx = self.getConnection()
        cursor = cnx.cursor()
        
        emp_no = 0
        try:
            cursor.execute(sql)
            emp_no = cursor.lastrowid
            cnx.commit()
        except Exception as e:
            emp_no = -1
            print("Run Error: ", sql)
            print(str(e))
        '''End Try'''  
        cursor.close()
        cnx.close()
        return emp_no
    
    def Query(self, sql, params, cnx = None, cursor = None):
        if not cnx: cnx = self.getConnection()
        if not cursor: 
            cursor = cnx.cursor()
            cursor.execute("BEGIN;")
        
        self.lsCurs.append(cursor)
        
        cursor.execute(sql, params)
        
        return cnx, cursor
    
    def begin(self):
        cnx = self.getConnection()
        cursor = cnx.cursor()
        cursor.execute("BEGIN;")
        return cnx, cursor
        
    '''似乎仅适用于原生连接'''
    def set_auto_commit(self, cnx, status):
        try:
            cnx.autocommit = True if status else False 
        except:
            print("Error when set autocommit=0")
    
    def QueryLine(self, cursor, sql, params):    
        cursor.execute(sql, params)
        res = cursor.fetchall()
        if not res or len(res) == 0: return None
        return res[0]
    
    def Transaction(self, lines, cnx = None, cursor = None, with_begin = True):
        if cnx==None: cnx = self.getConnection()
        if cursor==None: 
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        flag, lsRst = True, []
        '''开启事务'''
        if with_begin: cursor.execute("BEGIN;")
        try:
            for line in lines:
                cursor.execute(line[0], line[1])
                lsRst.append(cursor.lastrowid )
            cnx.commit()
        except Exception as e:
            cnx.rollback()
            flag = False                
            print("Run Error: ", lines)
            print(str(e))
        '''End For'''
        
        cursor.close()
        cnx.close()
        return flag, lsRst 
     
    def getKeys(self, tbName):
        return [info[0] for info in self.select("SHOW FULL COLUMNS FROM {}".format(tbName), ())]
    

if __name__ == '__main__':
    db = Database()
    print(db.getKeys("card"))
    
    