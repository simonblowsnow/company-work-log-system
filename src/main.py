#coding: utf8


from flask import Flask, request, current_app, g, render_template
from flask_cors import *
from functools import wraps
from src.libs.log import L
from src.libs.utils import TM, RandCode, DiffSecond
from src.common.key import KEY
from src.common.cache import RequestCache
from src.libs.redis2 import MyRedis as rs
from src.config import Web as C

from src.common.response import NormalResponseJson, NormalResponse, ErrorResponse, ErrorResponseJson, ErrorResponseData

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

import src.login as lg


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'AreUOK'
app.config['TOKEN_EXPIRATION'] = 7200


def check_ip_limit(ip):
    ftm = rs.hget(KEY.IPLimit, ip, False)
    if not ftm: return False
    '''封禁大约7天'''
    if DiffSecond(TM(), ftm) < 605000: return True
    
    return False

def getClientIP(request):
    ips = request.headers.get('X-Forwarded-For', '')
    return ips.split(',')[0].strip()

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
     
    g.user = {'user': data['user'], 'level': data['level'], 'scope': data['scope']}
    return True, "OK"

def authRequired(level):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            ip = getClientIP(request)
            if check_ip_limit(ip): return ErrorResponseJson("温馨提示：操作过于频繁，请稍后再试！")
            
            R = request.form if request.method=='POST' else request.args
            token, lc = R.get('tk', ''), R.get('lc', '')
            
            '''未提供token'''
            if token=='':
                return ErrorResponseJson("温馨提示：登录超时，请重新登陆！", None, '110') # 116-06
            flag, message = verify_password(token)
            '''token无效'''
            if not flag: 
                return ErrorResponseJson(message, None, '110')
            '''二次验证'''
            info = rs.hget('TKS', lc)
            
            if not info or info['tk'] != token:
                return ErrorResponseJson("登录超期，请重新登陆!", None, '110')
            
            '''权限检查'''
            U = rs.hget('UserInfo', info['user'])
            if not U or U['level'] < int(level[2:]): return ErrorResponseJson("权限不够或需要重新登陆！")
            
            '''此处可以优化，由装饰器控制返回结果'''
            res = RequestCache(func, info['user'], request, *args, **kwargs)

            return res
            
        return inner_wrapper
    return wrapper    

def webLoginCommon(request, app = None):
    ip = getClientIP(request)
    if check_ip_limit(ip): return ErrorResponseJson("温馨提示：操作过于频繁，请稍后再试！")
    
    R = request.form if request.method=='POST' else request.args
    client = str(R.get('mcode', '0'))
    securityCode, codeTms = str(R.get('securityCode', '')), str(R.get('tms', ''))
    correctCode = str(rs.hget('securityCode', codeTms, False))

    if not app and (codeTms=='' or securityCode=='' or correctCode!=securityCode):
        return ErrorResponseJson('验证码有误， 请重新输入！', None, '103-02')
    
    username, password = R.get('username', ''), R.get('password', '')
    
    data = lg.com_login(username, password, ip, "", app)
    if data['error']: return ErrorResponseData(data)
    
    L.log('User Login:', username, ip)
    token = get_token(username)
    uKey = str(abs(hash(token)) + 3456)
    
    '''TODO: 定期删除TKS或设置redis过期时间，防止太长'''
    U = data['data']
    userInfo = {'name': username, 'level': U['level'], 'point': U['point'], 'type': U['type'], 
                'allowTransfer': U['allowTransfer'], 'allowWithdraw': U['allowWithdraw'], 'id': U['id'], 
                'allowEqualCode': U['allowEqualCode'], 'defaultPasswd': U['defaultPasswd']}
    info = rs.hget('Users', uKey)
    if info and info['name'] != username: uKey += RandCode(6)
    '''踢除原登录用户·此处保留一个bug'''
    srcUKey = rs.hget(KEY.UserKey, username, False)
    if srcUKey: 
        rs.hdel('TKS', srcUKey)
        rs.hdel('Users', srcUKey)
    rs.hset('TKS', uKey, {'tk': token, 'user': username, 'time': TM()})
    rs.hset('Users', uKey, userInfo)
    rs.hset(KEY.UserInfo, username, userInfo)
    rs.hset(KEY.UserKey, username, uKey)
    
    data = {'u': username, 'tk': token, 'lc': uKey, 'lv': U['level'], "ip": ip, "client": client, "loginTime": TM() }
    print(data)
    
    return data

@app.route('/isLogin', methods=['GET', 'POST'])
@authRequired('lv0')
def isLogin(user):
    L.info("Request isLogin", user)
    return NormalResponseJson(request, {})

@app.route('/')
def index():
    return "Welcome..."

if __name__ == '__main__':
    L.info('server start on: {} !'.format(C.PORT))
    app.debug=False
    app.run(host='0.0.0.0', port=C.PORT)

