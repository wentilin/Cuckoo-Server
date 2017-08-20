#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from db import session_scope
from models import FeedComment

class FeedCommentProvider(object):
    @staticmethod
    def get_comment(cid):
        with session_scope() as session:
            comment = session.query(FeedComment).filter(FeedComment.id == cid).first()
            session.expunge_all()
            return comment

    @staticmethod
    def insert_comment(comment):
        with session_scope() as session:
            session.add(comment)
            session.commit()
            comm = session.query(FeedComment).filter(FeedComment.id == comment.id).first()
            session.expunge_all()
            return comm

    @staticmethod
    def delete_comment(cid):
        with session_scope() as session:
            comment = session.query(FeedComment).filter(FeedComment.id == cid).first()
            if comment:
                comment.status = 0

    @staticmethod
    def get_comments(fid, offset, size):
        with session_scope() as session:
            comments = session.query(FeedComment).filter(FeedComment.fid == fid, FeedComment.status == 1).order_by(FeedComment.cts.desc()).offset(offset).limit(size).all()
            session.expunge_all()
            return comments