"""[summary]
"""
import json
import sqlite3
from abc import ABCMeta, abstractmethod


class AbstractTelemetryStorage(metaclass=ABCMeta):
    """ Abstract Telemetry Storage class

    implements store_telemetry method that persists a given telemetry object

    Any class that stores the telemetry objects should be subclassed from
    this Abstract Class
    """
    # pylint: disable=too-few-public-methods

    @abstractmethod
    def store_telemetry(self, telemetry: dict) -> None:
        """ public method to persist telemetry object"""


class TelemetryInMemoryStorage(AbstractTelemetryStorage):
    """
    Class to provice telemetry in memory storage for use when unit testing
    """
    db_in_memory = None
    db_cursor = None

    def __init__(self):
        if not self.db_in_memory:
            self.initialize_db()

    @classmethod
    def initialize_db(cls):
        """
        class method to initialize the in memory db
        """
        if not cls.db_in_memory:
            cls.db_in_memory = \
                sqlite3.connect(":memory:")
            cls.db_cursor = cls.db_in_memory.cursor()
            cls._define_db_table(cls.db_cursor)

    @classmethod
    def close_db(cls):
        """close cursor and connections
        """
        cls.db_cursor.close()
        cls.db_in_memory.close()
        cls.db_cursor = None
        cls.db_in_memory = None

    @staticmethod
    def _define_db_table(cursor):
        """ define telemetry table """
        cursor.executescript('''
        DROP TABLE IF EXISTS telemetry;
        CREATE TABLE telemetry (process_name varchar(40),
        process_type varchar(40), start_date_time varchar(30),
        run_time varchar(20), telemetry_data json)''')

    def store_telemetry(self, telemetry: dict) -> None:
        """ public method to persist telemetry object"""
        telemetry_copy = telemetry.copy()
        process_name = telemetry_copy.pop('process_name', None)
        process_type = telemetry_copy.pop('process_type', None)
        start_date_time = telemetry_copy.pop('start_date_time', None)
        run_time_in_seconds = telemetry_copy.pop('run_time_in_seconds', None)
        json_object = json.dumps(telemetry_copy)

        self.db_cursor.execute(
            "insert into telemetry values (?, ?, ?, ?, ?)",
            [process_name, process_type, start_date_time,
             run_time_in_seconds, json_object]
        )
