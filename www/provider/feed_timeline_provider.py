#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from models import FeedTimeline
from db import session_scope


class FeedTimelineProvider(object):
    @staticmethod
    def insert_timeline_item(uid, fid, author_id, cts):
        with session_scope() as session:
            timeline = FeedTimeline(uid=uid, fid=fid, authorId=author_id, cts=cts)
            session.add(timeline)

    @staticmethod
    def hide_user_feeds(uid, author_id):
        with session_scope() as session:
            session.query(FeedTimeline).filter(FeedTimeline.uid == uid, FeedTimeline.authorId == author_id).delete(synchronize_session=False)
