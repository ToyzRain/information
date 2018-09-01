import random
import re
from info.lib.yuntongxun.sms import CCP
from flask import abort, jsonify
from flask import current_app
from flask import request, make_response
from info import constants
from info import redis_store
from info.models import User
from info.utlis.captcha.captcha import captcha
from info.module.passport import passport_bp
from info.utlis.response_code import RET


@passport_bp.route("/image_code")
def get_image():

    image_code_id = request.args.get("imageCodeId")

    # print(image_code_id)
    if not image_code_id:
        abort(404)

    name, text, image = captcha.generate_captcha()
    print(text)
    # 记得设置过期时长, ex可以从源码中看到 一定不要漏
    try:
        redis_store.set("image_code%s" % image_code_id, text, ex=constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        abort(500)

    response = make_response(image)
    response.headers["Content-Type"] = "image/jpeg"
    return response


# bug!!!!!!!!!!405错误, 漏了POST请求
@passport_bp.route("/sms_code", methods=["POST"])
def send_sms():
    """
    bug!!!!!!!!!!405错误, 漏了POST请求; 图形验证码如果存在就删除, 数据库查完之后!需要验证大小写!!!
    一定要判断用户是否已存在, 查询用户时候一定要加上first()
    """
    params_dict = request.json

    mobile = params_dict.get("mobile", None)
    image_code = params_dict.get("image_code", None)
    image_code_id = params_dict.get("image_code_id", None)

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    if not re.match(r'1[356789][0-9]{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式错误")

    try:
        real_image_code = redis_store.get("image_code%s" % image_code_id)
        # 图形验证码如果存在就删除, 查完之后!!!
        if real_image_code:
            redis_store.delete(real_image_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询验证码的真实值异常")

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码过期")

    # 需要验证大小写!!!
    if real_image_code.lower() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="验证码错误了")

    # 一定要判断用户是否已存在
    try:
        # 查询用户时候一定要加上first()
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询用户存在异常")
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号码注册过")

    sms_code = random.randint(0, 999999)
    sms_code = "%06d" % sms_code
    # current_app.logger.error(sms_code)
    # try:
    result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return
    if result:
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信验证码失败")

    try:
        redis_store.set("SMS_%s" % mobile, sms_code, ex=constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码到数据库异常")

    return jsonify(errno=RET.OK, errmsg="发送短信验证成功")
