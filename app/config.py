class Config:
    SECRET_KEY = 'dev'
    MYSQL_HOST = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DB = None
    MYSQL_PORT = None

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}