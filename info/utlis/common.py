from flask import current_app
from flask import g
from flask import session
# from info.models import User


def login_user_data(view_func):
    def wrapper(*args, **kwargs):
        user_id = session["user_id"]
        user = []

        from info.models import User
        if user_id:
            try:
                user = User.query.filter(User.id == user_id).first()
            except Exception as e:
                current_app.logger.error(e)

        g.user = user

        return view_func(*args, **kwargs)
    return wrapper
