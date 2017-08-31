#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from flask import request
from . import api, auth_required
from services.follow_service import FollowService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil


# 关注
@api.route('/friend/follow', methods=['POST'])
@auth_required
def follow(request, *, follow_uid):
    req = request.get_json()
    ReqUtil.not_null_params('follow_uid', **req)
    follow_uid = req.get('follow_uid')
    user = request.__user__

    FollowService.follow(user.id, follow_uid)

    return RespUtil.ok_response()


# 取消关注
@api.route('/friend/unFollow', methods=['POST'])
@auth_required
def un_follow():
    req = request.get_json()
    ReqUtil.not_null_params('follow_uid', **req)
    follow_uid = req.get('follow_uid')
    user = request.__user__

    FollowService.un_follow(user.id, follow_uid)

    return RespUtil.ok_response()


# 获取关注列表
@api.route('/friend/followers', methods=['POST'])
@auth_required
def followers():
    req = request.get_json()
    ReqUtil.not_null_params('page', 'size', **req)

    page = req['page']
    size = req['size']
    user = request.__user__
    uid = req.get('uid', user.id)

    arr = []

    followers = FollowService.get_followers(uid, page, size)
    data = {'page': page, 'count': len(followers)}
    for user in followers:
        item = {
            'uid': user.id,
            'name': user.name,
            'area': user.area,
            'avatar_url': user.avatarUrl,
            'signature': user.signature
        }

        if FollowService.has_follow(user.id, uid):
            item['followed'] = 1
        else:
            item['followed'] = 0

        arr.append(item)

    data['list'] = arr

    return RespUtil.ok_response(data)


# 获取粉丝列表
@api.route('/friend/followees', methods=['POST'])
@auth_required
def followees():
    req = request.get_json()
    ReqUtil.not_null_params('page', 'size', **req)

    page = req.get('page')
    size = req.get('size')
    user = request.__user__
    uid = req.get('uid', user.id)

    arr = []

    followers = FollowService.get_followees(uid, page, size)
    data = {'page': page, 'count': len(followers)}
    for user in followers:
        item = {
            'uid': user.id,
            'name': user.name,
            'area': user.area,
            'avatar_url': user.avatarUrl,
            'signature': user.signature
        }

        if FollowService.has_follow(uid, user.id):
            item['follow'] = 1
        else:
            item['follow'] = 0

        arr.append(item)

    data['list'] = arr

    return RespUtil.ok_response(data)
