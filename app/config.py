import os


class Config:
    SECRET_KEY = os.urandom(24)
    JSON_AS_ASCII = False  # json中文显示

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:111111@127.0.0.1:3306/atp?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_SECRET_KEY = 'atp'


class ProductConfig(Config):
    """
    正式环境
    """
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:111111@127.0.0.1:3306/py_test?charset=utf8'
    # SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'production': ProductConfig,
    'default': DevelopmentConfig
}

