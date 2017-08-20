#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from models import User
from db import session_scope
from utils.time_util import int_time


class UserProvider(object):
    @staticmethod
    def all():
        with session_scope() as session:
            users = session.query(User).all()
            session.expunge_all()
            return users

    @staticmethod
    def user_count():
        with session_scope() as session:
            users = session.query(User).count()
            return users

    @staticmethod
    def insert(user):
        with session_scope() as session:
            session.add(user)
            session.commit()
            u = session.query(User).filter(User.id == user.id).first()
            session.expunge_all()
            return u

    @staticmethod
    def get_user_by_phone(phone):
        with session_scope() as session:
            user = session.query(User).filter(User.phone == phone).first()
            session.expunge_all()
            return user

    @staticmethod
    def get_users_by_name(name):
        with session_scope() as session:
            users = session.query(User).filter(User.name == name).all()
            session.expunge_all()
            return users

    @staticmethod
    def get_user_by_id(uid):
        with session_scope() as session:
            user = session.query(User).filter(User.id == uid).first()
            session.expunge_all()
            return user

    @staticmethod
    def search_users(keyword):
        with session_scope() as session:
            keyword = '%' + keyword + '%'
            users = session.query(User).filter(User.name.like(keyword))
            session.expunge_all()
            return users

    @staticmethod
    def update_user_name(id, name):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.name = name
                user.uts = int_time()

    @staticmethod
    def update_user_avatar(id, avatar_url, avatar_url_origin):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.avatarUrl = avatar_url
                user.avatarUrlOrigin = avatar_url_origin
                user.uts = int_time()

    @staticmethod
    def update_user_gender(id, gender):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.gender = gender
                user.uts = int_time()

    @staticmethod
    def update_user_area(id, area):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.area = area
                user.uts = int_time()

    @staticmethod
    def update_user_signature(id, signature):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.signature = signature
                user.uts = int_time()

    @staticmethod
    def update_user_cover_url(id, cover_url):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.coverUrl = cover_url
                user.uts = int_time()

    @staticmethod
    def increment_follow_count(id):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.followCount += 1
                user.uts = int_time()

    @staticmethod
    def increment_followed_count(id):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user:
                user.followedCount += 1
                user.uts = int_time()

    @staticmethod
    def decrement_follow_count(id):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user and user.followCount > 0:
                user.followCount -= 1
                user.uts = int_time()

    @staticmethod
    def decrement_followed_count(id):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id, User.status == 1).first()
            if user and user.followedCount > 0:
                user.followedCount -= 1
                user.uts = int_time()
