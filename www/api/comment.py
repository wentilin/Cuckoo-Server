#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from flask import request
from . import api, auth_required
from utils.req_util import ReqUtil
from models import FeedComment
from services.feed_comment_service import FeedCommentService
from utils.resp_util import RespUtil


@api.route('/comment/create', methods=['POST'])
@auth_required
def create_comment():
    req = request.get_json()
    ReqUtil.not_null_params('fid', 'content', **req)

    fid = req['fid']
    content = req['content']
    toUid = req['toUid']
    toUname = req['toUname']
    user = request.__user__

    comment = FeedComment(fid=fid,
                          content=content,
                          uid=user.id,
                          uname=user.name,
                          avatarUrl=user.avatarUrl,
                          toUid=toUid,
                          toUname=toUname)
    new_comment = FeedCommentService.insert_comment(comment)

    return RespUtil.ok_response(data=_build_comment(new_comment))


@api.route('/comment/delete', methods=['POST'])
@auth_required
def delete_comment():
    req = request.get_json()
    ReqUtil.not_null_params('cid', **req)

    cid = req['cid']

    FeedCommentService.delete_comment(cid)
    return RespUtil.ok_response()


@api.route('/comment/list', methods=['POST'])
@auth_required
def comment_list():
    req = request.get_json()
    ReqUtil.not_null_params('fid', 'page', 'size',  **req)

    fid = req['fid']
    page = req['page']
    size = req['size']

    comments = FeedCommentService.get_comments(fid, page, size)

    return RespUtil.ok_response(_build_comment_list(page, comments))


def _build_comment_list(page, comments):
    data = {'page': page, 'count': len(comments)}

    array = []
    for comment in comments:
        item = {
            'id': comment.id,
            'uid': comment.uid,
            'fid': comment.fid,
            'user_name': comment.uname,
            'user_avatar_url': comment.avatarUrl,
            'to_uid': comment.toUid,
            'to_user_name': comment.toUname,
            'content': comment.content,
            'cts': comment.cts
        }

        array.append(item)

    data['list'] = array

    return data


def _build_comment(comment):
    item = {
        'id': comment.id,
        'uid': comment.uid,
        'fid': comment.fid,
        'user_name': comment.uname,
        'user_avatar_url': comment.avatarUrl,
        'to_uid': comment.toUid,
        'to_user_name': comment.toUname,
        'content': comment.content,
        'cts': comment.cts
    }

    return item
