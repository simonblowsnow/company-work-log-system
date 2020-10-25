#coding:utf8

from src.libs.database import Database
from src.libs.utils import TM, get_md5
from src.libs.log import L


def check_user_name(username):
    db = Database()
    sql = ("select * from user where username = %s")
    dt = db.selectEx(sql, (username, ))
    
    return len(dt) == 0

def com_login(user, passwd, ip, address = '', isApp = None):
    db = Database()
    sql = ("select password, status, level, nickname, type, id from user \
        where username = %s and isDel!=1")
    params = (user, )
    L.info("user {} login from ip: {}".format(user, ip))
    dt = db.selectEx(sql, params)
    rst = {'error':1, 'message':'success', 'data':{}}
    if len(dt)==0:
        rst['message'] = '用户不存在'
    elif dt[0][0]!=passwd and get_md5(dt[0][0])!=passwd:
        rst['message'] = '密码错误'
    else:
        if dt[0][1]!=0:
            rst['message'] = '用户登陆受限'
        else:
            rst['error'] = 0
            rst['data'] = {'level': dt[0][2], 'type': dt[0][4], 'id': dt[0][5], 
                           'nickname': dt[0][3].encode("utf8") if dt[0][3] else '未命名'
            }
    '''End If'''
    
    '''登陆成功'''
    if rst['error'] == 0:
        sqlU, paramsU = ("update user set loginTime = %s, onlineStatus = %s where \
            username = %s"), (TM(), 1, user)
        sqlL, paramsL = ("insert into logs (user, ip, address, client) values (%s, %s, %s, %s)"), \
            (user, ip, address, 'app' if isApp else 'pc')
        db.Transaction([[sqlU, paramsU], [sqlL, paramsL]])

    return rst

def loginOut(user, ip = '', address = ''):
    db = Database()
    
    sqlU, paramsU = ("update user set onlineStatus = %s where userName = %s"), (0, user)
    sqlL, paramsL = ("insert into logs (user, ip, style, createTime, address) values (%s, %s, 1, %s, %s)"), \
        (user, ip, TM(), address)
    db.Transaction([[sqlU, paramsU], [sqlL, paramsL]])

    return {}


def createUser():
    user = ['admin', '123456', 5, TM()]
    sql = "insert into user (username, password, level, createTime) values (%s, %s, %s, %s)"
    db = Database()
    db.execute(sql, user)
    
    
    
if __name__ == '__main__':
    createUser()
