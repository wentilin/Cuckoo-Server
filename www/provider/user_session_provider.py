from models import UserSession, User
from db import session_scope
from utils.time_util import int_time


class UserSessionProvider(object):
    @staticmethod
    def insert_session(uid, session_id, device):
        with session_scope() as session:
            user_session = UserSession(uid=uid, sessionId=session_id, device=device, cts=int_time(), uts=int_time())
            session.add(user_session)

    @staticmethod
    def get_session(session_id):
        with session_scope() as session:
            user_session = session.query(UserSession).\
                filter(UserSession.sessionId == session_id, UserSession.status == 1).first()
            session.expunge_all()
            return user_session

    @staticmethod
    def expire_session(uid, device):
        with session_scope() as session:
            session.query(UserSession).\
                filter(UserSession.uid == uid, UserSession.device == device, UserSession.status == 1).\
                update({UserSession.status: 0, UserSession.uts: int_time()}, synchronize_session=False)

    @staticmethod
    def get_session_by_uid(uid, device):
        with session_scope() as session:
            user_session = session.query(UserSession).\
                filter(UserSession.uid == uid, UserSession.device == device, UserSession.status == 1).\
                first()
            session.expunge_all()
            return user_session

