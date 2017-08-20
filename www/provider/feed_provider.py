#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import Feed, FeedVote, FeedTimeline
from db import session_scope
from utils.time_util import int_time


class FeedProvider(object):
    @staticmethod
    def insert_feed(feed):
        with session_scope() as session:
            session.add(feed)
            session.commit()
            f = session.query(Feed).filter(Feed.id == feed.id).first()
            session.expunge_all()
            return f

    @staticmethod
    def update_feed(feed):
        with session_scope() as session:
            feed.uts = int_time()
            session.merge(feed)

    @staticmethod
    def get_timeline(uid, offset, size):
        with session_scope() as session:
            sq = session.query(FeedTimeline.fid).filter(FeedTimeline.uid == uid).subquery()
            feeds = session.query(Feed).filter(Feed.id.in_(sq), Feed.status == 1).order_by(Feed.cts.desc()).offset(
                offset).limit(size).all()
            session.expunge_all()
            return feeds

    @staticmethod
    def get_user_feeds(uid, offset, size):
        with session_scope() as session:
            feeds = session.query(Feed).filter(Feed.uid == uid, Feed.status == 1).order_by(Feed.cts.desc()).offset(offset).limit(size).all()
            session.expunge_all()
            return feeds

    def get_like_list(uid, offset, size):
        with session_scope() as session:
            sq = session.query(FeedVote.fid).filter(FeedVote.uid==uid).subquery()
            feeds = session.query(Feed).filter(Feed.id.in_(sq), Feed.status == 1).order_by(Feed.cts.desc()).offset(
                offset).limit(size).all()
            session.expunge_all()
            return feeds

    @staticmethod
    def get_feed(id):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id == id, Feed.status == 1).first()
            session.expunge_all()
            return feed

    @staticmethod
    def delete_feed(fid, uid):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id==fid, Feed.uid==uid, Feed.status==1).first()
            feed.status = 0
            return True

    @staticmethod
    def increment_like_count(fid):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id == fid, Feed.status == 1).first()
            if feed:
                feed.likeCount += 1
                count = feed.likeCount
                return count

    @staticmethod
    def decrement_like_count(fid):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id == fid, Feed.status == 1).first()
            if feed and feed.likeCount > 0:
                feed.likeCount -= 1
                count = feed.likeCount
                return count

    @staticmethod
    def increment_comment_count(fid):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id == fid, Feed.status == 1).first()
            if feed:
                feed.commentCount += 1

    @staticmethod
    def decrement_comment_count(fid):
        with session_scope() as session:
            feed = session.query(Feed).filter(Feed.id == fid, Feed.status == 1).first()
            if feed and feed.commentCount > 0:
                feed.commentCount -= 1
