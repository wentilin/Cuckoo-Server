#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from provider.user_provider import UserProvider
from utils.string_util import StringUtil
from utils.int_util import IntUtil
from common.enums import VCardInfoType
import logging

class UserService(object):
    @staticmethod
    def get_user(uid):
        if uid is None or uid == 0:
            return None

        return UserProvider.get_user_by_id(uid)

    @staticmethod
    def search_users(keyword):
        if StringUtil.none_or_empty(keyword):
            return []

        return UserProvider.search_users(keyword)

    @staticmethod
    def update_user_info(vCard_type, user):
        if IntUtil.null_or_zero(user.id):
            return

        if vCard_type == VCardInfoType.AVATAR:
            UserProvider.update_user_avatar(user.id, user.avatarUrl, user.avatarUrlOrigin)
        elif vCard_type == VCardInfoType.NAME:
            UserProvider.update_user_name(user.id, user.name)
        elif vCard_type == VCardInfoType.GENDER:
            UserProvider.update_user_gender(user.id, user.gender)
        elif vCard_type == VCardInfoType.AREA:
            UserProvider.update_user_area(user.id, user.area)
        elif vCard_type == VCardInfoType.SIGNATURE:
            UserProvider.update_user_signature(user.id, user.signature)
        elif vCard_type == VCardInfoType.COVER:
            UserProvider.update_user_cover_url(user.id, user.coverUrl)
        else:
            logging.warning('Unknown VCardInfo type. type value is %s' % vCard_type)

