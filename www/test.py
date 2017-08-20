#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import database, asyncio
from models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from provider.user_provider import UserProvider
from provider.feed_provider import FeedProvider
from provider.user_session_provider import UserSessionProvider
from threading import Thread
import threading
from contextlib import contextmanager
from provider.feed_timeline_provider import FeedTimelineProvider
from provider.user_follow_provider import UserFollowProvider
import time

@contextmanager
def find_users(i):
    user = UserProvider.search_users('tiger')[0]
    print(threading.current_thread().name + str(i) + ':' + user.name)

async def test(loop):
    for i in range(0, 100000):
        Thread(target=find_users, args=(i,)).run()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
#loop.close()

