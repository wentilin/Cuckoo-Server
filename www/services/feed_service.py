#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import Feed, FeedTimeline, UserFollow
from common.constant import Constant
from utils.int_util import IntUtil
from provider.feed_provider import FeedProvider
from provider.feed_timeline_provider import FeedTimelineProvider
from provider.user_follow_provider import UserFollowProvider


class FeedService(object):
    @staticmethod
    def new_feed(feed):
        f = FeedProvider.insert_feed(feed)

        FeedTimelineProvider.insert_timeline_item(f.uid, f.id, f.uid, f.cts)

        follows = UserFollowProvider.get_user_followers(f.uid)
        for follow in follows:
            FeedTimelineProvider.insert_timeline_item(follow.uid, f.id, f.uid, f.cts)

        return f

    @staticmethod
    def get_timeline_feeds(uid, page, size):
        if page is None or page == 0:
            page = Constant.DEFAULT_PAGE

        if size is None or size == 0:
            size = Constant.DEFAULT_PAGE_SIZE

        feeds = FeedProvider.get_timeline(uid, (page-1)*size, size)
        return feeds

    @staticmethod
    def get_user_feeds(uid, page, size):
        if page is None or page == 0:
            page = Constant.DEFAULT_PAGE

        if size is None or size == 0:
            size = Constant.DEFAULT_PAGE_SIZE

        feeds = FeedProvider.get_user_feeds(uid, (page-1)*size, size)
        return feeds

    @staticmethod
    def get_like_list(uid, page, size):
        if page is None or page == 0:
            page = Constant.DEFAULT_PAGE

        if size is None or size == 0:
            size = Constant.DEFAULT_PAGE_SIZE

        feeds = FeedProvider.get_like_list(uid, (page-1)*size, size)
        return feeds

    @staticmethod
    def get_feed(fid):
        if IntUtil.null_or_zero(fid):
            return
        feed = FeedProvider.get_feed(fid)
        return feed

    @staticmethod
    def delete_feed(fid, uid):
        if IntUtil.null_or_zero(fid) or IntUtil.null_or_zero(uid):
            return False
        return FeedProvider.delete_feed(fid, uid)

    @staticmethod
    def distribute_feeds(uid, follow_uid):
        if IntUtil.null_or_zero(uid) or IntUtil.null_or_zero(follow_uid):
            return

        page = 1
        size = 100

        feeds = FeedService.get_user_feeds(follow_uid, page, size)
        while len(feeds) != 0:
            for feed in feeds:
                FeedTimelineProvider.insert_timeline_item(uid, feed.id, feed.uid, feed.cts)

            page += 1
            feeds = FeedService.get_user_feeds(follow_uid, page, size)

    @staticmethod
    def hide_user_feeds(uid, follow_uid):
        if IntUtil.null_or_zero(uid) or IntUtil.null_or_zero(follow_uid):
            return

        FeedTimelineProvider.hide_user_feeds(uid, follow_uid)

    @staticmethod
    def increment_like_count(fid):
        if IntUtil.null_or_zero(fid):
            return

        count = FeedProvider.increment_like_count(fid)
        return count

    @staticmethod
    def decrement_like_count(fid):
        if IntUtil.null_or_zero(fid):
            return

        count = FeedProvider.decrement_like_count(fid)
        return count

    @staticmethod
    def increment_comment_count(fid):
        if IntUtil.null_or_zero(fid):
            return

        FeedProvider.increment_comment_count(fid)

    @staticmethod
    def decrement_comment_count(fid):
        if IntUtil.null_or_zero(fid):
            return

        FeedProvider.decrement_comment_count(fid)
