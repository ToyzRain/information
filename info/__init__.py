import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from info.utlis.common import do_index_class

# 由于db后续会用到, 所有暴露出来
db = SQLAlchemy()
redis_store = None


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    app.add_template_filter(do_index_class)
    # 一定要调用才能创建日志
    create_log(config_name)

    db.init_app(app)

    # host='localhost', port=6379, db=0, decode_responses=False
    # 这里的配置必须要将二进制解码打开, 要不然后续的验证会一直不成功
    # 修改全局变量
    global redis_store
    redis_store = StrictRedis(host=config_dict[config_name].REDIS_HOST, port=config_dict[config_name].REDIS_PORT, db=config_dict[config_name].REDIS_NUM, decode_responses=True)

    # 这里是为了session会自动存储到redis中, Session的配置比较复杂
    Session(app)

    csrf = CSRFProtect(app)

    @app.after_request
    def set_csrf_token(response):
        # 调用函数生成 csrf_token
        csrf_token = generate_csrf()
        # 通过 cookie 将值传给前端
        response.set_cookie("csrf_token", csrf_token)
        return response

    from info.module.index import index_bp
    app.register_blueprint(index_bp)

    from info.module.passport import passport_bp
    app.register_blueprint(passport_bp)

    return app


def create_log(config_name):
    """记录日志的配置信息"""
    # 设置日志的记录等级
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # file_log_handler = RotatingFileHandler("logs/log", maxBytes=100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)