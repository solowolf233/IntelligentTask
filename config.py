# -*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #如果设置为True，Flask_SQLAlchemy将会追踪对象的修改，并且发出信号
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = True
    MAIL_PORT  = 25
    MAIL_USERNAME = '1252058937@qq.com'
    MAIL_PASSWORD = 'wbnpriobwmakigic'
    FLASKY_ADMIN = os.environ.get('MBH_ADMIN') or 'sun1252058937@163.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[MBH]'
    FLASKY_MAIL_SENDER = 'MBH Admin<1252058937@qq.com>'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')



config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}