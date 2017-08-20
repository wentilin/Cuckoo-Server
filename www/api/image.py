#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import time
import uuid
from urllib import parse

from PIL import Image

from config import configs
from corweb import get, post
from utils.encode_util import EncodeUtil
from utils.resp_util import RespUtil


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
