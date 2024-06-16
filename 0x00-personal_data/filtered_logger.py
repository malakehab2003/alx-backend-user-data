#!/usr/bin/env python3
""" create filter_datum function """
from typing import List
import re
import logging


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """ filter data and hide some data """
    for f in fields:
        message = re.sub(rf"{f}=(.*?)\{separator}",
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the record by filtering sensitive fields """
        original_message = super().format(record)
        filtered_message = filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR
        )
        return filtered_message
