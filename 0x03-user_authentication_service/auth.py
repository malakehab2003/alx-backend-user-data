#!/usr/bin/env python3
""" define _hash_password function """
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash a givin password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """ generate unique id """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ create new user with unique email """
        if email is None or password is None:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ check if valid login """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
            ):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ create new session """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ return user form session id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroy session """
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return None
        user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ update the reset token """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        new_id = _generate_uuid()
        user.reset_token = new_id
        return new_id

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
