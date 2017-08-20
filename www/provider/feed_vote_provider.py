#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from db import session_scope
from models import FeedVote

class FeedVoteProvider(object):
    @staticmethod
    def vote_is_exist(fid, uid):
        with session_scope() as session:
            count = session.query(FeedVote).filter(FeedVote.fid == fid, FeedVote.uid == uid).count()
            return True if count > 0 else False

    @staticmethod
    def insert_vote(vote):
        with session_scope() as session:
            session.add(vote)

    @staticmethod
    def delete_vote(fid, uid):
        with session_scope() as session:
            session.query(FeedVote).filter(FeedVote.fid == fid, FeedVote.uid == uid).delete(synchronize_session=False)

    @staticmethod
    def get_votes(fid, offset, size):
        with session_scope() as session:
            votes = session.query(FeedVote).filter(FeedVote.fid == fid).order_by(
            FeedVote.cts.desc()).offset(offset).limit(size).all()
            session.expunge_all()
            return votes

    @staticmethod
    def is_feed_liked(fid, uid):
        with session_scope() as session:
            count = session.query(FeedVote).filter(FeedVote.fid==fid, FeedVote.uid==uid).count()
            return True if count > 0 else False
