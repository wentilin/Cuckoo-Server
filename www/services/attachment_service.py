#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import Attachment
from provider.attachment_provider import AttachmentProvider


class AttachmentService(object):
    @staticmethod
    def insert(attachment):
        return AttachmentProvider.insert(attachment)

    @staticmethod
    def get_attachment(id):
        return AttachmentProvider.get_attachment(id)