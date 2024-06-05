#!/usr/bin/env python3
""" create the basic auth """


from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ create the basic auth """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                        ) -> str:
        """ encode the header """
        if (
            authorization_header is None or
            not isinstance(authorization_header, str) or
            authorization_header[:6] != 'Basic '
        ):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """ decode the header """
        if (
            base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)
        ):
            return None
        try:
            decoded_str = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            return decoded_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """ give email and password of the user """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ':' not in decoded_base64_authorization_header
        ):
            return None, None
        email_pass = decoded_base64_authorization_header.split(':')
        email = email_pass[0]
        password = email_pass[1]
        for i in range(2, len(email_pass)):
            word = ':' + email_pass[i]
            password += word
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """ return user instance based on email and password """
        if (
            user_email is None or
            user_pwd is None or
            not isinstance(user_pwd, str) or
            not isinstance(user_email, str)
        ):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if len(user) <= 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(
            self,
            request=None
    ) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
