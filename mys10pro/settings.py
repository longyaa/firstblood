from datetime import timedelta
from redis import Redis
from flask.sessions import SecureCookieSession
class Config(object):
    DEBUG = True
    SECRET_KEY = 'abcd'#session存cookie需要设置secret_key
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)

    #PERMANENT_SESSION_LIFETIME这个东西是设置session超时的，它来自于flasksessions里面的SecureCookieSession

    SESSION_REFRESH_EACH_REQUEST=True#设置session只要在20分钟内点击就不会失效
    SESSION_TYPE = "redis"#配置session的保存类型

class ProductionConfig(Config):
    SESSION_REDIS = Redis('127.0.0.1',port='6379')

class DevelopmentConfig(Config):
    SESSION_REDIS = Redis('127.0.0.1',port='6379')
class TestingConfig(Config):
    pass