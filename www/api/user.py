#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from flask import request
from . import api, auth_required
from common.enums import VCardInfoType
from services.follow_service import FollowService
from services.user_service import UserService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil


# 获取用户信息
@api.route('/user/vCard/<uid>', methods=['GET'])
@auth_required
def vCard(uid):
    ru = request.__user__
    user = UserService.get_user(uid)
    if user is None:
        return RespUtil.error_response(410, 'user not exist')

    ret = {
            'name': user.name,
            'avatar_url': user.avatarUrl,
            'avatar_url_origin': user.avatarUrlOrigin,
            'uid': user.id,
            'area': user.area if user.area else '',
            'gender': user.gender,
            'signature': user.signature if user.signature else '',
            'cover': user.coverUrl if user.coverUrl else '',
            'phone': user.phone,
            'follow_count': user.followCount,
            'followed_count': user.followedCount
           }
    if user.id == ru.id:
        ret['follow'] = 1
    else:
        if FollowService.has_follow(ru.id, user.id):
            ret['follow'] = 1
        else:
            ret['follow'] = 0

    return RespUtil.ok_response(ret)


# 更新用户信息
@api.route('/user/vCard', methods=['POST'])
@auth_required
def update_vcard():
    req = request.get_json()
    ReqUtil.not_null_params('type', 'value', **req)

    v_type = req['type']
    user = request.__user__

    value = req['value']

    vCard_type = VCardInfoType(v_type)
    if vCard_type == VCardInfoType.AVATAR:
        url1 = value.get('avatar_url', None)
        url2 = value.get('avatar_url_origin', None)

        if url1 is None or url2 is None:
            return RespUtil.error_response(405, 'Invalid params')

        user.avatarUrl = url1
        user.avatarUrlOrigin = url2
        UserService.update_user_info(vCard_type, user)
    elif vCard_type == VCardInfoType.NAME:
        user.name = value
        UserService.update_user_info(vCard_type, user)
    elif vCard_type == VCardInfoType.GENDER:
        if value == 0 or value == 1:
            user.gender = value
            UserService.update_user_info(vCard_type, user)
    elif vCard_type == VCardInfoType.AREA:
        user.area = value
        UserService.update_user_info(vCard_type, user)
    elif vCard_type == VCardInfoType.SIGNATURE:
        user.signature = value
        UserService.update_user_info(vCard_type, user)
    elif vCard_type == VCardInfoType.COVER:
        user.coverUrl = value
        UserService.update_user_info(vCard_type, user)
    else:
        return RespUtil.error_response(405, 'error type')

    return RespUtil.ok_response()


# 搜索用户
@api.route('/user/search', methods=['POST'])
@auth_required
def search_users():
    req = request.get_json()
    ReqUtil.not_null_params('keyword', **req)
    keyword = req.get('keyword')

    users = UserService.search_users(keyword)
    arr = []

    u = request.__user__

    for user in users:
        item = {
            'uid': user.id,
            'name': user.name,
            'area': user.area,
            'avatar_url': user.avatarUrl,
            'signature': user.signature
        }

        if FollowService.has_follow(u.id, user.id):
            item['follow'] = 1
        else:
            item['follow'] = 0

        arr.append(item)

    return RespUtil.ok_response(arr)
