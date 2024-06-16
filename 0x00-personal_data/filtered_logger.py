#!/usr/bin/env python3
""" create filter_datum function """
from typing import List
import re
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """ get logger function """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Implement db conectivity
    """
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main() -> None:
    """ the main function """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    for data in cursor:
        message = f"name={data[0]}; email={data[1]}; phone={data[2]}; " +\
            f"ssn={data[3]}; password={data[4]};ip={data[5]}; " +\
            f"last_login={data[6]}; user_agent={data[7]};"
        print(message)
    cursor.close()
    conn.close()


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



if __name__ == '__main__':
    """ main function """
    main()
