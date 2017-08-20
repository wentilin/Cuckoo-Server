#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from provider.user_follow_provider import UserFollowProvider
from services.feed_service import FeedService
from provider.user_provider import UserProvider
from common.constant import Constant
from utils.int_util import IntUtil


class FollowService(object):
    @staticmethod
    def has_follow(uid, follow_uid):
        if IntUtil.null_or_zero(uid) or IntUtil.null_or_zero(follow_uid):
            return False

        return UserFollowProvider.has_follow(uid, follow_uid)

    @staticmethod
    def follow(uid, follow_uid):
        if IntUtil.null_or_zero(uid) or IntUtil.null_or_zero(follow_uid):
            return

        UserFollowProvider.follow(uid, follow_uid)
        UserProvider.increment_follow_count(uid)
        UserProvider.increment_followed_count(follow_uid)
        FeedService.distribute_feeds(uid, follow_uid)

    @staticmethod
    def un_follow(uid, follow_uid):
        if IntUtil.null_or_zero(uid) or IntUtil.null_or_zero(follow_uid):
            return

        UserFollowProvider.unfollow(uid, follow_uid)
        UserProvider.decrement_follow_count(uid)
        UserProvider.decrement_followed_count(follow_uid)
        FeedService.hide_user_feeds(uid, follow_uid)

    @staticmethod
    def get_followers(uid, page, size):
        if IntUtil.null_or_zero(uid):
            return []

        if IntUtil.null_or_zero(page):
            page = Constant.DEFAULT_PAGE

        if IntUtil.null_or_zero(size):
            size = Constant.DEFAULT_PAGE_SIZE

        offset = (page - 1) * size
        users = UserFollowProvider.get_followers(uid, offset, size)

        return users

    @staticmethod
    def get_followees(uid, page, size):
        if IntUtil.null_or_zero(uid):
            return []

        if IntUtil.null_or_zero(page):
            page = Constant.DEFAULT_PAGE

        if IntUtil.null_or_zero(size):
            size = Constant.DEFAULT_PAGE_SIZE

        offset = (page - 1) * size
        users = UserFollowProvider.get_followees(uid, offset, size)

        return users
