#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from api.errors import APIParamError


class ReqUtil(object):
    @staticmethod
    def not_null_params(*keys, **kw):
        if keys is None or len(keys) == 0:
            return

        for key in keys:
            value = kw.get(key, None)
            if value is None:
                raise APIParamError(str(key) + ' can not be null!')
