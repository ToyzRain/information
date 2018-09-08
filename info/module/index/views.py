from info import constants
from info.models import News
from info.module.index import index_bp
from flask import render_template, current_app, g
from info.utlis.common import login_user_data


@index_bp.route("/")
@login_user_data
def index():

    user = g.user

    try:
        news_model = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_list = []
    for news in news_model if news_model else []:
        news_dict_list.append(news.to_dict())

    data = {
        "user_info": user.to_dict() if user else None,
        "newsClickList": news_dict_list,
    }
    # print(data)
    print(current_app.url_map)
    return render_template("index.html", data=data)


@index_bp.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")


# 显示用户信息是不需要额外接口的
# @index_bp.route("/")
