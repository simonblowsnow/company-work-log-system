#coding:utf8

from functools import wraps
from flask import current_app, g, request
from src.libs.utils import DiffSecond
from src.common.key import KEY
from src.common.cache import RequestCache
from src.libs.redis2 import MyRedis as rs
from src.libs.database import Database
from src.libs.utils import TM, get_md5
from src.libs.log import L
from src.common.response import ErrorResponseJson, ErrorResponseData
from src.libs.auth_code import create_validate_code
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


def check_user_name(username):
    db = Database()
    sql = ("select * from user where username = %s")
    dt = db.selectEx(sql, (username, ))
    
    return len(dt) == 0

def user_login(user, passwd, ip, address = '', isApp = None):
    db = Database()
    sql = ("select password, status, level, nickname, type, id from user \
        where username = %s and isDel!=1")
    params = (user, )
    L.info("user {} login from ip: {}".format(user, ip))
    dt = db.selectEx(sql, params)
    rst = {'error':1, 'message':'success', 'data':{}}
    print(dt)
    
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

def login_out(user, ip = '', address = ''):
    del_token(user)
    db = Database()
    
    sqlU, paramsU = ("update user set onlineStatus = %s where userName = %s"), (0, user)
    sqlL, paramsL = ("insert into logs (user, ip, style, createTime, address) values (%s, %s, 1, %s, %s)"), \
        (user, ip, TM(), address)
    db.Transaction([[sqlU, paramsU], [sqlL, paramsL]])

    return {}


'''--------------------------------通用服务器用户体系逻辑------------------------------------------'''
def auth_required(level):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            ip = get_client_ip(request)
            if check_ip_limit(ip): return ErrorResponseJson("温馨提示：操作过于频繁，请稍后再试！")
            
            '''token存放于headers的Authorization中'''
            # token = request.headers.get('Authorization', '')
            R = request.form if request.method=='POST' else request.args
            token = R.get('token', '')
            
            '''未提供token'''
            if token == '': return ErrorResponseJson("温馨提示：登录超时，请重新登陆！", None, '110')
            flag, message = verify_password(token)
            '''token无效'''
            if not flag: return ErrorResponseJson(message, None, '110')
            
            username = g.user['username']
            '''二次验证'''
            tk = rs.hget(KEY.TOKENS, hash_token(token, username), False)
            
            if not tk: return ErrorResponseJson("登录超期，请重新登陆!", None, '110')
            
            '''权限检查'''
            U = rs.hget(KEY.USERS, username)
            if not U or U['level'] < int(level[2:]): return ErrorResponseJson("权限不够或需要重新登陆！")
            
            '''此处可以优化，由装饰器控制返回结果'''
            res = RequestCache(func, username, request, *args, **kwargs)

            return res
            
        return inner_wrapper
    return wrapper    

def web_login_common(request, no_code = False):
    ip = get_client_ip(request)
    if check_ip_limit(ip): return ErrorResponseJson("温馨提示：操作过于频繁，请稍后再试！")
    
    R = request.form if request.method=='POST' else request.args
    client = str(R.get('mcode', '0'))
    securityCode, codeTms = str(R.get('securityCode', '')), str(R.get('tms', ''))
    correctCode = str(rs.hget('securityCode', codeTms, False))

    if not no_code and (codeTms=='' or securityCode=='' or correctCode!=securityCode):
        return ErrorResponseJson('验证码有误， 请重新输入！', None, '103-02')
    
    username, password = R.get('username', ''), R.get('password', '')
    data = user_login(username, password, ip, "", no_code)
    if data['error']: return ErrorResponseData(data)
    
    L.info('User Login: %s, %s' % (username, ip))
    '''TODO: 定期删除TKS或设置redis过期时间，防止太长'''
    U = data['data']
    user_info = {'name': username, 'level': U['level'], 'type': U['type'], 'id': U['id'] }
    '''记录用户和登录信息'''
    token = create_token(username, user_info)
    
    data = {'u': username, 'tk': token, 'lv': U['level'], "ip": ip, "client": client, "loginTime": TM() }
    
    return data

def hash_token(token, username):
    return str(get_md5(token)) + "_" + username

def create_token(username, user_info):
    '''若存在登录则剔除原用户'''
    del_token(username)
    
    token = get_token(username)
    key = hash_token(token, username)
    user_info['tk'] = key 
    rs.hset(KEY.TOKENS, key, {'level': user_info['level'], 'time': TM()})
    rs.hset(KEY.USERS, username, user_info)
    
    return token

'''删除token，请求中二次验证时将无法通过'''
def del_token(username):
    info = rs.hget(KEY.USERS, username)
    if info: 
        rs.hdel(KEY.TOKENS, info['tk'])
        rs.hdel(KEY.USERS, username)

def get_token(username, level = 0, scope = "1"):
    expiration = current_app.config['TOKEN_EXPIRATION']
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({ 'user': username, 'level': level, 'scope': scope })
    return token.decode('ascii')

def verify_password(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        return False, "温馨提示：登录超时，请重新登陆！" # 'token is invalid'
    except SignatureExpired:
        return False, 'token is expired'
    '''End try'''
     
    g.user = {'username': data['user'], 'level': data['level'], 'scope': data['scope']}
    return True, "OK"

'''返回图形验证码·需要提供时间参数'''
def get_auth_code(app):
    params = list(request.args.items())
    if len(params) == 0: return ''
    tms = params[0][0]
    bufStr, codeStr = create_validate_code()

    response = app.make_response(bufStr)
    response.headers['Content-Type'] = 'image/png'
    '''存储待验证'''
    rs.hset('securityCode', tms, codeStr)

    return response

def get_client_ip(request):
    ips = request.headers.get('X-Forwarded-For', '')
    return ips.split(',')[0].strip()

'''IP黑名单功能'''
def check_ip_limit(ip):
    ftm = rs.hget(KEY.IP_LIMIT, ip, False)
    if not ftm: return False
    '''封禁大约7天'''
    if DiffSecond(TM(), ftm) < 605000: return True
    
    return False

'''---------------------------------------End·通用用户逻辑----------------------------------------------'''


def createUser():
    user = ['admin', '123456', 5, TM()]
    sql = "insert into user (username, password, level, createTime) values (%s, %s, %s, %s)"
    db = Database()
    db.execute(sql, user)
    
    
    
if __name__ == '__main__':
#     createUser()
    pass
    
    
    