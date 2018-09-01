from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# 由于db后续会用到, 所有暴露出来
db = SQLAlchemy()
redis_store = None


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    db.init_app(app)

    # host='localhost', port=6379, db=0, decode_responses=False
    # 这里的配置必须要将二进制解码打开, 要不然后续的验证会一直不成功
    # 修改全局变量
    global redis_store
    redis_store = StrictRedis(host=config_dict[config_name].REDIS_HOST, port=config_dict[config_name].REDIS_PORT, db=config_dict[config_name].REDIS_NUM, decode_responses=True)

    # 这里是为了session会自动存储到redis中, Session的配置比较复杂
    Session(app)

    csrf = CSRFProtect(app)

    return app