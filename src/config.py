#coding: utf8

class Mysql():
    HOST = "106.54.48.46"
    PORT = 3306
    DB_NAME = "testDB"
    USER_NAME = "root"
    PASSWORD = "root"
    TB_NAME = ""
    POOL_SIZE = 3
    
    HOST = "106.54.48.46"
    PASSWORD = "simonblowsnow"

class Redis():
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