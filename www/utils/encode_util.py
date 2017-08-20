#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


import uuid
import hashlib
import time

class EncodeUtil(object):
    @staticmethod
    def md5(content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()


    @staticmethod
    def new_salt(account):
        id = str(uuid.uuid4())

        return EncodeUtil.md5(id)

    @staticmethod
    def new_session_id():
        timestamp = str(time.time())

        return EncodeUtil.md5(timestamp)