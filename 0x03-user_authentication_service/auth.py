#!/usr/bin/env python3
""" define _hash_password function """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash a givin password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
