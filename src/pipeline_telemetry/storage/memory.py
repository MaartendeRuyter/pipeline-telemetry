"""[summary]
"""
import json
import sqlite3
from typing import Optional

from ..data_classes import TelemetryModel
from ..settings import settings as st
from .generic import AbstractTelemetryStorage


class TelemetryInMemoryStorage(AbstractTelemetryStorage):
    """
    Class to provice telemetry in memory storage for use when unit testing
    """

    db_in_memory: Optional[sqlite3.Connection] = None
    db_cursor: Optional[sqlite3.Cursor] = None

    def __init__(self):
        if not self.db_in_memory:
            self.initialize_db()

    @classmethod
    def initialize_db(cls) -> None:
        """
        class method to initialize the in memory db
        """
        if not cls.db_in_memory:
            cls.db_in_memory = sqlite3.connect(":memory:")
            cls.db_cursor = cls.db_in_memory.cursor()
            cls._define_db_table(cls.db_cursor)

    @classmethod
    def close_db(cls) -> None:
        """close cursor and connections"""
        if cls.db_cursor:
            cls.db_cursor.close()

        if cls.db_in_memory:
            cls.db_in_memory.close()

        cls.db_cursor = None
        cls.db_in_memory = None

    @staticmethod
    def _define_db_table(cursor):
        """define telemetry table"""
        cursor.executescript(
            """
            DROP TABLE IF EXISTS telemetry;
            CREATE TABLE telemetry (telemetry_type varchar(100),
            category varchar(60), sub_category varchar(60),
            source_name varchar(40), process_type varchar(40),
            start_date_time timestamp, run_time varchar(20),
            telemetry_data json, traffic_light varchar(10),
            io_time_in_seconds real)"""
        )

    # def store_telemetry_old(self, telemetry: dict) -> None:
    #     """public method to persist telemetry object"""
    #     telemetry_copy = telemetry.copy()
    #     telemetry_type = telemetry_copy.pop(st.TELEMETRY_TYPE_KEY, None)
    #     category = telemetry_copy.pop(st.CATEGORY_KEY, None)
    #     sub_category = telemetry_copy.pop(st.SUB_CATEGORY_KEY, None)
    #     source_name = telemetry_copy.pop(st.SOURCE_NAME_KEY, None)
    #     process_type = telemetry_copy.pop(st.PROCESS_TYPE_KEY, None)
    #     start_date_time = telemetry_copy.pop(st.START_TIME, None)
    #     run_time_in_seconds = telemetry_copy.pop(st.RUN_TIME, None)
    #     traffic_light = telemetry_copy.pop(st.TRAFFIC_LIGHT_KEY, None)
    #     io_time_in_seconds = telemetry_copy.pop(st.IO_TIME_KEY, None)
    #     json_object = json.dumps(telemetry_copy)

    #     if self.db_cursor:
    #         self.db_cursor.execute(
    #             "insert into telemetry values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #             [
    #                 telemetry_type,
    #                 category,
    #                 sub_category,
    #                 source_name,
    #                 process_type,
    #                 start_date_time,
    #                 run_time_in_seconds,
    #                 json_object,
    #                 traffic_light,
    #                 io_time_in_seconds
    #             ],
    #         )

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        telemetry_type = getattr(telemetry, st.TELEMETRY_TYPE_KEY)
        category = getattr(telemetry, st.CATEGORY_KEY)
        sub_category = getattr(telemetry, st.SUB_CATEGORY_KEY)
        source_name = getattr(telemetry, st.SOURCE_NAME_KEY)
        process_type = getattr(telemetry, st.PROCESS_TYPE_KEY)
        start_date_time = getattr(telemetry, st.START_TIME)
        run_time_in_seconds = getattr(telemetry, st.RUN_TIME)
        traffic_light = getattr(telemetry, st.TRAFFIC_LIGHT_KEY)
        io_time_in_seconds = getattr(telemetry, st.IO_TIME_KEY)
        telemetry_data = {
            k: v.__dict__ for k, v in
            getattr(telemetry, st.TELEMETRY_FIELD_KEY).items()
        }
        json_object = json.dumps(telemetry_data)

        if self.db_cursor:
            self.db_cursor.execute(
                "insert into telemetry values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    telemetry_type,
                    category,
                    sub_category,
                    source_name,
                    process_type,
                    start_date_time,
                    run_time_in_seconds,
                    json_object,
                    traffic_light,
                    io_time_in_seconds
                ],
            )
