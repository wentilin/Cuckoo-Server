#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from corweb import post
from utils.req_util import ReqUtil
from models import FeedComment
from services.feed_comment_service import FeedCommentService
from utils.resp_util import RespUtil

@post('/api/v1/comment/create', auth=True)
def create_comment(request, **kw):
    ReqUtil.not_null_params('fid', 'content', **kw)

    fid = kw['fid']
    content = kw['content']
    toUid = kw['toUid']
    toUname = kw['toUname']
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


@post('/api/v1/comment/delete', auth=True)
def delete_comment(**kw):
    ReqUtil.not_null_params('cid', **kw)

    cid = kw['cid']

    FeedCommentService.delete_comment(cid)
    return RespUtil.ok_response()


@post('/api/v1/comment/list', auth=True)
def comment_list(**kw):
    ReqUtil.not_null_params('fid', 'page', 'size',  **kw)

    fid = kw['fid']
    page = kw['page']
    size = kw['size']

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



