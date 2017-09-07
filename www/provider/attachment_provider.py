#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import Attachment
from db import session_scope


class AttachmentProvider(object):
    @staticmethod
    def insert(attachment):
        with session_scope() as session:
            session.add(attachment)
            session.commit()
            id = attachment.id
            session.expunge_all()
            attachment.id = id

            return attachment

    @staticmethod
    def get_attachment(id):
        with session_scope() as session:
            a = session.query(Attachment).filter(Attachment.id==id).first()
            session.expunge_all()
            return a