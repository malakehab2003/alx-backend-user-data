#!/usr/bin/env python3
""" create auth class """
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """ manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        for i in excluded_paths:
            if i[-1] == '*':
                pattern = r"^(.*)\*"
                match = re.match(pattern, i)
                part_without_star = match.group(1)
                if path.startswith(part_without_star):
                    return False
                else:
                    return True
        if path and path[-1] != '/':
            path = path + '/'
        if (excluded_paths is None or
                path is None or
                path not in excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
    
    def session_cookie(self, request=None) -> str:
        """ create session_cookie function """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
