#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import uuid

import time
from flask import request, abort, send_from_directory

from config import configs
from services.attachment_service import AttachmentService
from utils.encode_util import EncodeUtil
from . import api, auth_required
from models import Attachment
from utils.resp_util import RespUtil
import cv2

# 上传文件
@api.route('/attachment/upload', methods=['POST'])
#@auth_required
def attachment_upload():
    file = request.files['file']
    if file is None:
        return RespUtil.error_response(404, 'file not found')
    if file.filename is None:
        return RespUtil.error_response(405, 'file name not found')

    components = file.filename.split('.')
    if len(components) < 2:
        return RespUtil.error_response(406, 'file extension not found')
    file_ext = components[-1]
    name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time()))

    file_path = os.path.join(configs.resource_path, name + '.' + file_ext)


    attachment = Attachment(uid=7,
                            name=name,
                            filename=components[0],
                            extension=file_ext,
                            size=file.content_length)
    a = AttachmentService.insert(attachment)

    file.save(file_path)

    cap = cv2.VideoCapture(file_path)
    img_name = EncodeUtil.md5(str(uuid.uuid4()) + str(time.time())) + '.jpg'
    img_path = os.path.join(configs.resource_path, img_name)
    if cap.isOpened():
        ret, image = cap.read()
        (h, w) = image.shape[:2]
        center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, -90, 1.0)
        rotated_img = cv2.warpAffine(image, M, (w, h))

        cv2.imwrite(img_path, rotated_img)

    cap.release()

    cover_img = 'http://' + request.host + '/image/' + img_name
    return RespUtil.ok_response({'file_id': a.id, 'file_type': file_ext, 'cover_img': cover_img})


# 下载文件
@api.route('/attachment/<id>', methods=['GET'])
#@auth_required
def attachment_download(id):
    a = AttachmentService.get_attachment(id)
    if a is None:
        abort(404)

    filename = a.name + '.' + a.extension
    if os.path.isfile(os.path.join(configs.resource_path, filename)):
        return send_from_directory(configs.resource_path, filename, as_attachment=True)
    else:
        abort(404)
