#!/usr/bin/env python3
""" create class SessionAuth """
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a new session """
        if user_id is None or not isinstance(user_id, str):
            return None
        new_id = str(uuid4())
        self.user_id_by_session_id[new_id] = user_id
        return new_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ create function user_id_for_session_id """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
