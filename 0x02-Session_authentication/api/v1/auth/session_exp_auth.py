#!/usr/bin/env python3
""" expire the session after time """
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ expire the session after some time """
    def __init__(self):
        """ constructor """
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ create session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ create user_id_for_session_id method """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session_dict['created_at'] + time_span
        if exp_time < cur_time:
            return None
        return session_dict['user_id']
