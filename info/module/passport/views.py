from flask import abort
from flask import request, make_response

from info import constants
from info import redis_store
from info.utlis.captcha.captcha import captcha
from info.module.passport import passport_bp


@passport_bp.route("/image_code")
def get_image():

    image_code_id = request.args.get("imageCodeId")

    print(image_code_id)
    if not image_code_id:
        abort(404)

    name, text, image = captcha.generate_captcha()
    print(text)
    # 记得设置过期时长, ex可以从源码中看到
    try:
        redis_store.set("image_code%s" % image_code_id, text, ex=constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        abort(500)

    response = make_response(image)
    response.headers["Content-Type"] = "image/jpeg"
    return response
