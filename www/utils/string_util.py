#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


class StringUtil(object):
    @staticmethod
    def none_or_empty(string):
        if string is None or string.strip() == '':
            return True
        else:
            return False