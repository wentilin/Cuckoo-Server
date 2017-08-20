#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from provider.feed_comment_provider import FeedCommentProvider
from services.feed_service import FeedService
from utils.int_util import IntUtil
from common.constant import Constant

class FeedCommentService(object):
    @staticmethod
    def insert_comment(comment):
        if comment is None:
            return

        comm = FeedCommentProvider.insert_comment(comment)
        FeedService.increment_comment_count(comm.fid)

        return comm

    @staticmethod
    def delete_comment(cid):
        if IntUtil.null_or_zero(cid):
            return

        FeedCommentProvider.delete_comment(cid)
        comment = FeedCommentProvider.get_comment(cid)
        FeedService.decrement_comment_count(comment.fid)

    @staticmethod
    def get_comments(fid, page, size):
        if page is None or page == 0:
            page = Constant.DEFAULT_PAGE

        if size is None or size == 0:
            size = Constant.DEFAULT_PAGE_SIZE

        return FeedCommentProvider.get_comments(fid, (page-1)*size, size)
