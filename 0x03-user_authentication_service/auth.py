#!/usr/bin/env python3
""" define _hash_password function """
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ hash a givin password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


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
        except:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError(f'User {email} already exists')
