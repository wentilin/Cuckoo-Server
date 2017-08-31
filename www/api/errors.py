#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


class APIError(Exception):
    def __init__(self, code, data='', msg=''):
        super(APIError, self).__init__(msg)
        self.code = code
        self.data = data
        self.msg = msg

class APIValueError(APIError):
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

class APIPermissionError(APIError):
    def __init__(self, msg=''):
        super(APIPermissionError, self).__init__(406, 'permission', msg)

class APIParamError(APIError):
    def __init__(self, msg=''):
        super(APIParamError, self).__init__(400, msg=msg)