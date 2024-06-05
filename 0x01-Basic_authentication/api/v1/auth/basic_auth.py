#!/usr/bin/env python3
""" create the basic auth """


from .auth import Auth


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
