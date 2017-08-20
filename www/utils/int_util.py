#! /usr/bin/env python3
# _*_ coding: utf-8 _*_


class IntUtil(object):
    @staticmethod
    def null_or_zero(num):
        if type(num) != int or num == 0:
            return True
        else:
            return False
