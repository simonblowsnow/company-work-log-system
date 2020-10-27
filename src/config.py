#coding: utf8

class Mysql():
    HOST = "106.54.48.46"
    PORT = 3306
    USER_NAME = "root"
    PASSWORD = "root"
    DB_NAME = "company_wrok_log"
    TB_NAME = ""
    POOL_SIZE = 4
    
    HOST = "106.54.48.46"
    PASSWORD = "simonblowsnow"

class Redis():
    '''开发模式下redis遇到错误会切换至本地存储模式，可在无redis服务器的情况下运行'''
    DEV_MODE = True
    HOST = "106.54.48.46"
    PORT = 6379
    DB_NAME = "3"
    USER_NAME = "root"
    PASSWORD = "root"
    
    
    PORT = 60379
    PASSWORD = "chuixue123"

class Web():        
    PORT = 9406
    
    
class Config():
    mysql = Mysql
    redis = Redis
    web = Web