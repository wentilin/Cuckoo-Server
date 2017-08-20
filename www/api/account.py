#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from corweb import post
from services.account_service import AccountService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil
from utils.string_util import StringUtil


# 验证姓名和手机号是否存在
@post('/api/v1/account/validate')
def validate(**kw):
    ReqUtil.not_null_params('field', 'value', **kw)

    field = int(kw.get('field'))
    value = kw.get('value')

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
@post('/api/v1/account/signIn')
def signin(**kw):
    ReqUtil.not_null_params('account', 'password', **kw)

    account = kw.get('account')
    passwd = kw.get('password')
    device = kw.get('device', 0)

    if StringUtil.none_or_empty(account) or StringUtil.none_or_empty(passwd):
        return RespUtil.error_response(401, '账户名和密码不能为空.')

    user = AccountService.signin(account, passwd)
    if user is None:
        return RespUtil.error_response(400, '用户名或密码错误.')

    session_id = AccountService.build_session(user, device)

    return RespUtil.built_user_response(user, session_id)


# 用户注册
@post('/api/v1/account/signUp')
def signup(**kw):
    ReqUtil.not_null_params('name', 'phone', 'avatar_url', 'avatar_url_origin', 'gender', 'password', **kw)

    name = kw.get('name')
    phone = kw.get('phone')
    avatar_url = kw.get('avatar_url')
    avatar_url_origin = kw.get('avatar_url_origin')
    gender = kw.get('gender')
    password = kw.get('password')

    added = AccountService.add_new_user(name, phone, avatar_url, avatar_url_origin, gender, password)
    if added:
        return RespUtil.ok_response()
    else:
        return RespUtil.error_response(405, '注册失败')


# 用户退出
@post('/api/v1/account/signOut', auth=True)
def signout(request):
    user = request.__user__
    AccountService.expire_session(user.id, user.device)

    return RespUtil.ok_response()
