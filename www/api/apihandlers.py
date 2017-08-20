#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import asyncio
import hashlib
import json
import logging
import os
import time
import uuid
from json import JSONDecoder
from urllib import parse

from PIL import Image

from common.enums import VCardInfoType
from config import configs
from corweb import get, post
from models import Feed
from services.account_service import AccountService
from services.feed_service import FeedService
from services.follow_service import FollowService
from services.user_service import UserService
from utils.encode_util import EncodeUtil
from utils.req_util import ReqUtil
from utils.resp_util import RespUtil
from utils.string_util import StringUtil

COOKIE_NAME = 'coolblogsession'
_COOKIE_KEY = configs.session.secret


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError:
        pass
    return 1 if p < 1 else p


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


def user2cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    l = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(l)


@asyncio.coroutine
def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        l = cookie_str.split('-')
        if len(l) != 3:
            return None
        uid, expires, sha1 = l
        if int(expires) < time.time():
            return None
        user = UserService.get_user(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


@get('/test')
def test():
    users = UserService.search_users('tiger')
    return RespUtil.ok_response(users)


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
        RespUtil.error_response(400, '用户名或密码错误.')

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


# 获取用户信息
@get('/api/v1/user/vCard/{uid}', auth=True)
def vCard(request, *, uid):
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
@post('/api/v1/user/vCard', auth=True)
def update_vcard(request, **kw):
    ReqUtil.not_null_params('type', 'value', **kw)

    v_type = kw['type']
    user = request.__user__

    value = kw['value']

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
@post('/api/v1/user/search', auth=True)
def search_users(request, *, keyword):
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


# 发表动态
@post('/api/v1/feed/publish', auth=True)
def new_feed(request, **kw):
    ReqUtil.not_null_params('title', 'desc', 'coverImg', 'content', **kw)

    title = kw.get('title')
    desc = kw.get('desc')
    coverImg = kw.get('coverImg')
    content = JSONDecoder().decode(kw.get('content'))

    user = request.__user__
    feed = Feed()
    feed.uid = user.id
    feed.title = title
    feed.desc = desc
    feed.coverImg = coverImg
    feed.content = json.dumps(content, ensure_ascii=False).encode('utf-8')

    FeedService.new_feed(feed)

    return RespUtil.ok_response()


# 获取用户feed列表
@post('/api/v1/feed/list', auth=True)
def feed_list(request, **kw):
    ReqUtil.not_null_params('page', 'size', **kw)

    page = kw.get('page')
    size = kw.get('size')

    uid = kw.get('uid', None)
    if uid and uid == 0:
        return RespUtil.error_response(405, 'invalid uid')
    else:
        uid = request.__user__.id

    feeds = FeedService.get_user_feeds(uid, page, size)

    return RespUtil.ok_response(_build_feed_list(page, feeds))


# 获取feed详情
@post('/api/v1/feed/detail', auth=True)
def feed_detail(*, fid=None):
    if fid is None:
        return RespUtil.error_response(405, 'invalid fid')
    feed = FeedService.get_feed(fid)
    if feed is None:
        return RespUtil.error_response(409, 'feed not exist')

    data = {
        'id': feed.id,
        'title': feed.title,
        'coverImg': feed.coverImg,
        'desc': feed.desc,
        'cts': feed.cts,
        'content': JSONDecoder().decode(feed.content)
    }

    return RespUtil.ok_response(data)


# 获取timeline
@post('/api/v1/feed/timeline', auth=True)
def feed_timeline(request, **kw):
    ReqUtil.not_null_params('page', 'size', **kw)

    page = kw.get('page')
    size = kw.get('size')

    feeds = FeedService.get_timeline_feeds(request.__user__.id, page, size)

    return RespUtil.ok_response(_build_feed_list(page, feeds))


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


def _build_feed_list(page, feeds):
    data = {'page': page, 'count': len(feeds)}

    array = []
    for feed in feeds:
        user = UserService.get_user(feed.uid)
        if user is None:
            continue

        item = {
            'id': feed.id,
            'uid': feed.uid,
            'user_name': user.name,
            'user_avatar_url': user.avatarUrl,
            'title': feed.title,
            'coverImg': feed.coverImg,
            'desc': feed.desc,
            'cts': feed.cts
        }

        array.append(item)

    data['list'] = array

    return data


# 上传图片
@post('/image/upload')
def image_upload(request):
    reader = yield from request.multipart()
    img_data = yield from reader.next()
    img_name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time()))
    thumb_img_name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time()))
    img_path = os.path.join(configs.resource_path, img_name)
    thumb_img_path = os.path.join(configs.resource_path, thumb_img_name)
    qs = request.query_string
    size = (600, 600)
    if qs:
        for k, v in parse.parse_qs(qs, True).items():
            if k == 'size' and v and len(v) > 0:
                size = v[0].split('x')
                size[0] = int(size[0])
                size[1] = int(size[1])
                if len(size) == 2:
                    if size[0] < 100:
                        w = 100
                        h = (100 // size[0]) * size[1]
                        size = (w, h)
                    elif size[1] < 100:
                        h = 100
                        w = (100 // size[1]) * size[0]
                        size = (w, h)
                    else:
                        size = (size[0], size[1])
                else:
                    size = (600, 600)
                break
            else:
                continue

    with open(img_path, 'wb') as f:
        while True:
            chunk = yield from img_data.read_chunk()
            if not chunk:
                break
            f.write(chunk)
        f.close()
        img = Image.open(img_path)
        img.thumbnail(size, Image.NEAREST)
        img.save(thumb_img_path, 'JPEG')

        return RespUtil.ok_response({'url': 'http://' + request.host + '/image/' + img_name,
                                     'thumb_url': 'http://' + request.host + '/image/' + thumb_img_name
                                     })


# 获取图片资源
@get('/image/{id}')
def get_image(id):
    file_path = configs.resource_path + '/' + id
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            return data
    except:
        return RespUtil.error_response(404, 'file not found')
