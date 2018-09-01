from redis import StrictRedis


class Config(object):

    DEBUG = True
    SECRET_KEY = "Cnv8TxO7QxCQ2wdrHji1y4NjuqFFQXWnTbnVoRJUbjIiFWraasJKReYD1O/F4Hb9"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/re_information"
    # 配置的是app的上下文结束后自动提交数据库的修/删
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_NUM = 6

    SESSION_TYPE = "redis"
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_NUM, decode_responses=True)
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
