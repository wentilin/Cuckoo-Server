#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from enum import Enum


class VCardInfoType(Enum):
    INVALID   = -1
    AVATAR    = 0
    NAME      = 1
    GENDER    = 2
    AREA      = 3
    SIGNATURE = 4
    COVER     = 5

    @staticmethod
    def parse(type):
        try:
            return VCardInfoType(type)
        except:
            return VCardInfoType.INVALID