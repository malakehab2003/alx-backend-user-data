#!/usr/bin/env python3
""" create the user session to store session in file """
from .base import Base


class UserSession(Base):
    """ create user session to store session """
    def __init__(self, *args: list, **kwargs: dict):
        """ constructor """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get('session_id')
