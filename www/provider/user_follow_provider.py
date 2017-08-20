#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from models import UserFollow, User
from db import session_scope
from utils.time_util import int_time


class UserFollowProvider(object):
    @staticmethod
    def follow(uid, follow_uid):
        with session_scope() as session:
            follow = UserFollow(uid=uid, followUid=follow_uid, cts=int_time())
            session.add(follow)

    @staticmethod
    def unfollow(uid, follow_id):
        with session_scope() as session:
            session.query(UserFollow).filter(UserFollow.uid == uid, UserFollow.followUid == follow_id).delete(
                synchronize_session=False)

    @staticmethod
    def get_user_followers(uid):
        with session_scope() as session:
            followers = session.query(UserFollow).filter(UserFollow.followUid == uid).all()
            session.expunge_all()
            return followers

    @staticmethod
    def get_following_users(uid):
        with session_scope() as session:
            following_users = session.query(UserFollow).filter(UserFollow.uid == uid).all()
            session.expunge_all()
            return following_users

    @staticmethod
    def get_followers(uid, offset, size):
        with session_scope() as session:
            sq = session.query(UserFollow.followUid).filter(UserFollow.uid == uid).subquery()
            users = session.query(User).filter(User.id.in_(sq), User.status == 1).offset(offset).limit(size).all()
            session.expunge_all()
            return users

    @staticmethod
    def get_followees(uid, offset, size):
        with session_scope() as session:
            sq = session.query(UserFollow.uid).filter(UserFollow.followUid == uid).subquery()
            users = session.query(User).filter(User.id.in_(sq), User.status == 1).offset(offset).limit(size).all()
            session.expunge_all()
            return users

    @staticmethod
    def has_follow(uid, target_uid):
        with session_scope() as session:
            count = session.query(UserFollow).filter(UserFollow.uid == uid, UserFollow.followUid == target_uid).count()
            return count > 0