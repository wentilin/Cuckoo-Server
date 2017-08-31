#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

engine = create_engine('mysql+pymysql://www-data:www-data@localhost:3306/cuckoodb?charset=utf8mb4',
                       pool_size=100,
                       pool_recycle=3600)
DBSession = sessionmaker(bind=engine)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

@contextmanager
def session_scope():
    session = db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

