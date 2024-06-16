#!/usr/bin/env python3
""" hash the password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
