from info.module.index import index_bp
from flask import render_template, current_app
from info import models


@index_bp.route("/")
def index():

    print(current_app.url_map)
    return render_template("index.html")


@index_bp.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")


# 显示用户信息是不需要额外接口的
# @index_bp.route("/")
