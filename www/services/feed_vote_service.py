#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import FeedVote
from provider.feed_vote_provider import FeedVoteProvider
from utils.int_util import IntUtil
from utils.string_util import StringUtil
from common.constant import Constant

class FeedVoteService(object):
    @staticmethod
    def insert_vote(fid, uid, uname, avatarUrl):
        if IntUtil.null_or_zero(fid) or \
                IntUtil.null_or_zero(uid) or \
                StringUtil.none_or_empty(uname) or \
                StringUtil.none_or_empty(avatarUrl):
            return False

        if FeedVoteProvider.vote_is_exist(fid, uid):
            return False

        vote = FeedVote(fid=fid, uid=uid, uname=uname, avatarUrl=avatarUrl)

        FeedVoteProvider.insert_vote(vote)

        return True

    @staticmethod
    def delete_vote(fid, uid):
        if IntUtil.null_or_zero(fid) or IntUtil.null_or_zero(uid):
            return False

        if FeedVoteProvider.vote_is_exist(fid, uid):
            FeedVoteProvider.delete_vote(fid, uid)
            return True

        return False

    @staticmethod
    def get_votes(fid, page, size):
        if page is None or page == 0:
            page = Constant.DEFAULT_PAGE

        if size is None or size == 0:
            size = Constant.DEFAULT_PAGE_SIZE

        return FeedVoteProvider.get_votes(fid, (page-1)*size, size)

    @staticmethod
    def is_feed_liked(fid, uid):
        return FeedVoteProvider.is_feed_liked(fid, uid)
