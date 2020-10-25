#coding:utf8

from src.libs.redis2 import MyRedis as rs
from src.libs.log import L
from src.libs.utils import TMS

'''缓存'''
CacheData = {}
CacheFuncList = dict((item[0], {'args': item[1], 'seconds': item[2]}) for item in [
    ["queryBalance", ["user"], 60] 
    
])

count = 0

def RequestCache(func, user, request, *args, **kwargs):    
    global count
    fn = func.__name__
    if fn not in CacheFuncList: return func(user, *args, **kwargs)
    
    R = request.form if request.method=='POST' else request.args
    fnKey, params, seconds = fn, CacheFuncList[fn]['args'], CacheFuncList[fn]['seconds']
    for p in params: fnKey += "_" + (user if p == "user" else R.get(p, ''))
    
    count += 1
    res = None
    
    if not rs.hexists('CacheData', fnKey):
        res = func(user, *args, **kwargs)
        rs.hset('CacheData', fnKey, {'time': TMS(), 'data': res})
    else:
        ca = rs.hget('CacheData', fnKey)
        if (TMS() - ca['time']) / 1000 < seconds: 
            count -= 1
            return ca['data']  
        res = func(user, *args, **kwargs)
        rs.hset('CacheData', fnKey, {'time': TMS(), 'data': res})
    
    count -= 1
    return res


