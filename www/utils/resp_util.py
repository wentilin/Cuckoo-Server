#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from flask import jsonify

class RespUtil(object):

    @staticmethod
    def ok_response(data=None):
        if data is None:
            return jsonify(code=200, msg='OK')
        else:
            return jsonify(code=200, msg='OK', data=data)


    @staticmethod
    def error_response(code, msg):
        return jsonify(code=code, msg=msg)

    @staticmethod
    def built_user_response(user, seesion_id):
        data = {
            'name': user.name,
            'uid': user.id,
            'phone': user.phone,
            'gender': user.gender,
            'avatar_url': user.avatarUrl,
            'session_id': seesion_id
        }

        return RespUtil.ok_response(data=data)