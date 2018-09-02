from info.module.index import index_bp
from flask import render_template, current_app, g
from info.utlis.common import login_user_data


@index_bp.route("/")
@login_user_data
def index():

    user = g.user

    data = {
        "user_info": user.to_dict() if user else None
    }
    # print(data)
    print(current_app.url_map)
    return render_template("index.html", data=data)


@index_bp.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")


# 显示用户信息是不需要额外接口的
# @index_bp.route("/")
