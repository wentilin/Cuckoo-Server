#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from corweb import post
from services.follow_service import FollowService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil


# 关注
@post('/api/v1/friend/follow', auth=True)
def follow(request, *, follow_uid):
    user = request.__user__
    FollowService.follow(user.id, follow_uid)

    return RespUtil.ok_response()


# 取消关注
@post('/api/v1/friend/unFollow', auth=True)
def un_follow(request, *, follow_uid):
    user = request.__user__
    FollowService.un_follow(user.id, follow_uid)

    return RespUtil.ok_response()


# 获取关注列表
@post('/api/v1/friend/followers', auth=True)
def followers(request, **kw):
    ReqUtil.not_null_params('page', 'size', **kw)

    page = kw['page']
    size = kw['size']
    user = request.__user__
    uid = kw.get('uid', user.id)

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
@post('/api/v1/friend/followees', auth=True)
def followees(request, **kw):
    ReqUtil.not_null_params('page', 'size', **kw)

    page = kw.get('page')
    size = kw.get('size')
    user = request.__user__
    uid = kw.get('uid', user.id)

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
