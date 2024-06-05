#!/usr/bin/env python3
""" create the basic auth """


from .auth import Auth
import base64


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
        """ encode email and password of the user """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ':' not in decoded_base64_authorization_header
        ):
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password
