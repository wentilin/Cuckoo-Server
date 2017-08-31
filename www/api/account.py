#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from . import api
from services.account_service import AccountService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil
from utils.string_util import StringUtil
from flask import request
from . import auth_required


# 验证姓名和手机号是否存在
@api.route('/account/validate', methods=['POST'])
def validate():
    req = request.get_json()
    ReqUtil.not_null_params('field', 'value', **req)
    field = int(req.get('field'))
    value = req.get('value')
    # 0-name, 1-phone
    if field == 1:
        if AccountService.user_exist_by_name(value):
            return RespUtil.error_response(407, '该昵称已经被使用，请更换另一个')
    elif field == 2:
        if AccountService.user_exist_by_phone(value):
            return RespUtil.error_response(407, '该手机号已经注册！')
    else:
        return RespUtil.error_response(407, 'Error field, field is undefined')

    return RespUtil.ok_response()


# 用户登录
@api.route('/account/signIn', methods=['POST'])
def signin():
    req = request.get_json()
    ReqUtil.not_null_params('account', 'password', **req)

    account = req.get('account')
    passwd = req.get('password')
    device = req.get('device', 0)

    if StringUtil.none_or_empty(account) or StringUtil.none_or_empty(passwd):
        return RespUtil.error_response(401, '账户名和密码不能为空.')

    user = AccountService.signin(account, passwd)
    if user is None:
        return RespUtil.error_response(400, '用户名或密码错误.')

    session_id = AccountService.build_session(user, device)

    return RespUtil.built_user_response(user, session_id)


# 用户注册
@api.route('/account/signUp', methods=['POST'])
def signup():
    req = request.get_json()
    ReqUtil.not_null_params('name', 'phone', 'avatar_url', 'avatar_url_origin', 'gender', 'password', **req)

    name = req.get('name')
    phone = req.get('phone')
    avatar_url = req.get('avatar_url')
    avatar_url_origin = req.get('avatar_url_origin')
    gender = req.get('gender')
    password = req.get('password')

    added = AccountService.add_new_user(name, phone, avatar_url, avatar_url_origin, gender, password)
    if added:
        return RespUtil.ok_response()
    else:
        return RespUtil.error_response(405, '注册失败')


# 用户退出
@api.route('/account/signOut', methods=['POST'])
@auth_required
def sign_out():
    user = request.__user__
    AccountService.expire_session(user.id, user.device)

    return RespUtil.ok_response()
