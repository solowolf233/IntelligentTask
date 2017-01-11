# coding:utf-8
import json
from flask import session, make_response, Flask, request, render_template
from geetest import GeetestLib
from . import captcha
import random


captcha_id = "7ed2e53ba9a32e8c072dee22ad53b06a"
private_key = "b59c65bd4b3d180b1a62b77fc81533d2"


@captcha.route('/register', methods=["GET"])
def get_captcha():
    user_id = random.randint(1,10000)
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str


@captcha.route('/validate', methods=["POST"])
def validate_capthca():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
        print 111
    else:
        result = gt.failback_validate(challenge, validate, seccode)
        print 222
    result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
    return result

@captcha.route('/ajax_validate', methods=["POST"])
def ajax_validate():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    user_id = session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    result = {"status":"success"} if result else {"status":"fail"}
    return json.dumps(result)

@captcha.route('/')
def login():
    return render_template('/auth/test.html')