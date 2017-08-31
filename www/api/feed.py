#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
from json import JSONDecoder
from flask import request
from . import api, auth_required
from models import Feed
from services.feed_service import FeedService
from services.user_service import UserService
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil
from services.feed_vote_service import FeedVoteService


# 发表动态
@api.route('/feed/publish', methods=['POST'])
@auth_required
def new_feed():
    req = request.get_json()
    ReqUtil.not_null_params('title', 'desc', 'coverImg', 'content', **req)

    title = req.get('title')
    desc = req.get('desc')
    coverImg = req.get('coverImg')
    content = JSONDecoder().decode(req.get('content'))

    user = request.__user__
    feed = Feed()
    feed.uid = user.id
    feed.title = title
    feed.desc = desc
    feed.coverImg = coverImg
    feed.content = json.dumps(content, ensure_ascii=False).encode('utf-8')

    feed = FeedService.new_feed(feed)

    return RespUtil.ok_response(_build_feed(feed, request.__user__))


# 获取用户feed列表
@api.route('/feed/list', methods=['POST'])
@auth_required
def feed_list():
    req = request.get_json()
    ReqUtil.not_null_params('page', 'size', **req)

    page = req.get('page')
    size = req.get('size')

    uid = req.get('uid', None)
    if uid:
        if uid == 0:
            return RespUtil.error_response(405, 'invalid uid')
    else:
        uid = request.__user__.id

    feeds = FeedService.get_user_feeds(uid, page, size)

    return RespUtil.ok_response(_build_feed_list(page, feeds))


# 获取feed详情
@api.route('/feed/detail', methods=['POST'])
@auth_required
def feed_detail():
    req = request.get_json()
    ReqUtil.not_null_params('fid', **req)

    fid = req.get('fid')
    feed = FeedService.get_feed(fid)
    if feed is None:
        return RespUtil.error_response(409, 'feed not exist')
    user = UserService.get_user(feed.uid)
    liked = FeedVoteService.is_feed_liked(feed.id, request.__user__.id)
    data = {
        'id': feed.id,
        'uid': feed.uid,
        'uname': user.name,
        'avatar_url': user.avatarUrl,
        'title': feed.title,
        'coverImg': feed.coverImg,
        'desc': feed.desc,
        'liked': 1 if liked else 0,
        'comment_count': feed.commentCount,
        'like_count': feed.likeCount,
        'cts': feed.cts,
        'content': JSONDecoder().decode(feed.content)
    }

    return RespUtil.ok_response(data)


# 获取feed详情
@api.route('/feed/delete', methods=['POST'])
@auth_required
def delete_feed():
    req = request.get_json()
    ReqUtil.not_null_params('fid', **req)

    fid = req.get('fid')
    if FeedService.delete_feed(fid, request.__user__.id):
        return RespUtil.ok_response()
    else:
        return RespUtil.error_response(407, 'delete failed')


# 获取timeline
@api.route('/feed/timeline', methods=['POST'])
@auth_required
def feed_timeline():
    req = request.get_json()
    ReqUtil.not_null_params('page', 'size', **req)

    page = req.get('page')
    size = req.get('size')

    feeds = FeedService.get_timeline_feeds(request.__user__.id, page, size)

    return RespUtil.ok_response(_build_feed_list(page, feeds))


# 获取喜欢列表
@api.route('/feed/likelist', methods=['POST'])
@auth_required
def feed_like_list():
    req = request.get_json()
    ReqUtil.not_null_params('page', 'size', **req)

    page = req.get('page')
    size = req.get('size')

    uid = req.get('uid', None)
    if uid:
        if uid == 0:
            return RespUtil.error_response(405, 'invalid uid')
    else:
        uid = request.__user__.id

    feeds = FeedService.get_like_list(uid, page, size)

    return RespUtil.ok_response(_build_feed_list(page, feeds))


# 点赞
@api.route('/feed/vote', methods=['POST'])
@auth_required
def vote():
    req = request.get_json()
    ReqUtil.not_null_params('fid', **req)

    user = request.__user__
    fid = req.get('fid')

    if FeedVoteService.insert_vote(fid, user.id, user.name, user.avatarUrl):
        count = FeedService.increment_like_count(fid)
        return RespUtil.ok_response(data={"like_count": count})
    else :
        return RespUtil.error_response(407, '已经点过赞，不可重复!')


# 取消点赞
@api.route('/feed/unvote', methods=['POST'])
@auth_required
def unvote():
    req = request.get_json()
    ReqUtil.not_null_params('fid', **req)

    user = request.__user__
    fid = req.get('fid')

    if FeedVoteService.delete_vote(fid, user.id):
        count = FeedService.decrement_like_count(fid)
        return RespUtil.ok_response(data={"like_count": count})
    else:
        return RespUtil.error_response(code=407, msg='并没有点赞，取消无效!')


def _build_feed_list(page, feeds):
    data = {'page': page, 'count': len(feeds)}

    array = []
    for feed in feeds:
        user = UserService.get_user(feed.uid)
        if user is None:
            continue

        item = _build_feed(feed, user)

        array.append(item)

    data['list'] = array

    return data


def _build_feed(feed, user):
    return {
            'id': feed.id,
            'uid': feed.uid,
            'user_name': user.name,
            'user_avatar_url': user.avatarUrl,
            'title': feed.title,
            'coverImg': feed.coverImg,
            'desc': feed.desc,
            'cts': feed.cts,
            'like_count': feed.likeCount,
            'comment_count': feed.commentCount
        }
