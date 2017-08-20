#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from models import User
from provider.user_provider import UserProvider
from provider.user_session_provider import UserSessionProvider
from utils.encode_util import EncodeUtil
from utils.string_util import StringUtil


class AccountService(object):
    def __init__(self):
        super(AccountService, self).__init__()

    # 有效账户返回用户信息，否则返回None
    @staticmethod
    def signin(account, passwd):
        if StringUtil.none_or_empty(account) or StringUtil.none_or_empty(passwd):
            return None

        user = UserProvider.get_user_by_phone(account)
        if user and AccountService._validate_passwd(passwd, user):
            return user

        return None

    @staticmethod
    def add_new_user(name, phone, avatar_url, avatar_url_origin, gender, password):
        exist = AccountService.user_exist(phone)
        if exist:
            return False

        user = User(name=name, phone=phone, avatarUrl=avatar_url, avatarUrlOrigin=avatar_url_origin, gender=gender)

        salt = EncodeUtil.new_salt(phone)
        user.salt = salt
        user.passwd = EncodeUtil.md5(password + salt)

        UserProvider.insert(user)

        return True

    @staticmethod
    def user_exist(account):
        user = UserProvider.get_user_by_phone(account)

        return True if user else False

    @staticmethod
    def user_exist_by_name(name):
        users = UserProvider.get_users_by_name(name)

        return False if len(users) == 0 else True

    @staticmethod
    def user_exist_by_phone(phone):
        user = UserProvider.get_user_by_phone(phone)

        return True if user else False

    @staticmethod
    def _validate_passwd(passwd, user):
        salt = user.salt
        encode = EncodeUtil.md5(passwd + salt)
        if encode == user.passwd:
            return True

        return False

    @staticmethod
    def build_session(user, device):
        UserSessionProvider.expire_session(user.id, device)

        session_id = EncodeUtil.new_session_id()
        UserSessionProvider.insert_session(user.id, session_id, device)

        return session_id

    @staticmethod
    def expire_session(uid, device):
        UserSessionProvider.expire_session(uid, device)

    @staticmethod
    def auth(uid, device, code, date):
        if code is None:
            return None

        session = UserSessionProvider.get_session_by_uid(uid, device)
        if session is None:
            return None

        auth_code = EncodeUtil.md5('%s%s%s%s' % (uid, device, date, session.sessionId))
        if auth_code == code:
            user = UserProvider.get_user_by_id(uid)
            return user

        return None
