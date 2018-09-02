import functools
from flask import current_app
from flask import g
from flask import session
# from info.models import User


def login_user_data(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = []

        # 为了避免循环导入, 哪里用哪里导
        from info.models import User
        if user_id:
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        g.user = user
        result = view_func(*args, **kwargs)
        return result
    return wrapper
