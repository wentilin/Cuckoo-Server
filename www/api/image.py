#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import time
import uuid
from PIL import Image

from flask import request, send_from_directory, abort
from . import img_api
from config import configs
from utils.encode_util import EncodeUtil
from utils.resp_util import RespUtil


# 上传图片
@img_api.route('/image/upload', methods=['POST'])
def image_upload():
    file = request.files['file']
    if file is None:
        return RespUtil.error_response(404, 'file not found')

    img_name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time()))
    thumb_img_name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time()))
    img_path = os.path.join(configs.resource_path, img_name)
    thumb_img_path = os.path.join(configs.resource_path, thumb_img_name)
    qs = request.args.get('size')
    size = (600, 600)
    if qs and len(qs) > 0:
        size = qs.split('x')
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

    file.save(img_path)
    img = Image.open(img_path)
    img.thumbnail(size, Image.NEAREST)
    img.save(thumb_img_path, 'JPEG')

    return RespUtil.ok_response({'url': 'http://' + request.host + '/image/' + img_name,
                                 'thumb_url': 'http://' + request.host + '/image/' + thumb_img_name
                                 })


# 获取图片资源
@img_api.route('/image/<id>', methods=['GET'])
def get_image(id):
    file_path = configs.resource_path
    if os.path.isfile(os.path.join(file_path, id)):
        return send_from_directory(file_path, id, as_attachment=True)
    else:
        abort(404)
