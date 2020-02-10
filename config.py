import os


# configuration

class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_ENABLED = True


class TestingConfig(Config):
    DATABASE = '/tmp/zhenmiao.db'
    SQLALCHEMY_DATABAASE_URI = 'sqlite:///' + DATABASE


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
