#!/usr/bin/env python3
""" create filter_datum function """
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
):
    """ filter data and hide some data """
    pattern = '|'.join(f'{field}=[^{"{sep}"}]*'
                       .format(sep=re.escape(separator)) for field in fields)
    return re.sub(pattern, lambda m: m.group(0)
                  .split('=')[0] + f'={redaction}', message)
