#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import time
import uuid
from utils.time_util import int_time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, SmallInteger, DateTime, Text

Base = declarative_base()


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    phone = Column(String(32), unique=True)
    avatarUrl = Column(String(128))
    avatarUrlOrigin = Column(String(128))
    gender = Column(SmallInteger, default=0)
    passwd = Column(String(128))
    salt = Column(String(64))
    cts = Column(DateTime, default=int_time)
    uts = Column(DateTime, default=int_time)
    area = Column(String(64))
    coverUrl = Column(String(128))
    signature = Column(String(128))
    followCount = Column(Integer, default=0)
    followedCount = Column(Integer, default=0)
    status = Column(SmallInteger, default=1)


class UserFollow(Base):
    __tablename__ = 'user_follow'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(BigInteger)
    followUid = Column(BigInteger)
    cts = Column(DateTime, default=int_time)


class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(BigInteger)
    sessionId = Column(String(128))
    cts = Column(DateTime, default=int_time)
    uts = Column(DateTime, default=int_time)
    status = Column(SmallInteger, default=1)
    device = Column(SmallInteger, default=0)


class Feed(Base):
    __tablename__ = 'feed'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(BigInteger)
    title = Column(String(64))
    coverImg = Column(String(128))
    desc = Column(String(256))
    content = Column(Text)
    cts = Column(DateTime, default=int_time)
    uts = Column(DateTime, default=int_time)
    status = Column(SmallInteger, default=1)
    shareCode = Column(String(64))
    likeCount = Column(Integer, default=0)
    commentCount = Column(Integer, default=0)


class FeedTimeline(Base):
    __tablename__ = 'feed_timeline'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(BigInteger)
    fid = Column(BigInteger)
    authorId = Column(BigInteger)
    cts = Column(DateTime, default=int_time)


class FeedComment(Base):
    __tablename__ = 'feed_comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(BigInteger)
    uid = Column(BigInteger)
    uname = Column(String(50))
    avatarUrl = Column(String(128))
    toUid = Column(BigInteger, default=0)
    toUname = Column(String(50))
    content = Column(Text)
    cts = Column(DateTime, default=int_time)
    status = Column(SmallInteger, default=1)


class FeedVote(Base):
    __tablename__ = 'feed_vote'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(BigInteger)
    uid = Column(BigInteger)
    uname = Column(String(50))
    avatarUrl = Column(String(128))
    cts = Column(DateTime, default=int_time)
