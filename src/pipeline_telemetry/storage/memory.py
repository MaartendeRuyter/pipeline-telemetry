"""[summary]"""

import json
import sqlite3
from datetime import datetime
from typing import Iterator, Optional

from ..data_classes import TelemetryModel
from ..settings import exceptions
from ..settings import settings as st
from .generic import AbstractTelemetryStorage


def dict_factory(cursor, row):
    """Method to allow sql queries to be returned as a dict.

    The telemetry field is seperately converted to a dict because
    sqlite returns a nested dict as a string.
    """
    col_names = [col[0] for col in cursor.description]
    telemetry = {key: value for key, value in zip(col_names, row)}
    telemetry_str = telemetry.pop("telemetry", "{}")
    telemetry.update({"telemetry": json.loads(telemetry_str)})
    return telemetry


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
            cls.db_in_memory.row_factory = dict_factory
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
            start_date_time timestamp, run_time_in_seconds varchar(20),
            telemetry json, traffic_light varchar(10),
            io_time_in_seconds real)"""
        )

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        if not self.db_cursor:
            raise exceptions.StorageNotInitialized

        telemetry_type = getattr(telemetry, st.TELEMETRY_TYPE_KEY)
        category = getattr(telemetry, st.CATEGORY_KEY)
        sub_category = getattr(telemetry, st.SUB_CATEGORY_KEY)
        source_name = getattr(telemetry, st.SOURCE_NAME_KEY)
        process_type = getattr(telemetry, st.PROCESS_TYPE_KEY)
        start_date_time = getattr(telemetry, st.START_TIME).isoformat()
        run_time_in_seconds = getattr(telemetry, st.RUN_TIME)
        traffic_light = getattr(telemetry, st.TRAFFIC_LIGHT_KEY)
        io_time_in_seconds = getattr(telemetry, st.IO_TIME_KEY)
        telemetry_dict = {
            k: v.__dict__ for k, v in getattr(telemetry, st.TELEMETRY_FIELD_KEY).items()
        }
        telemetry_json = json.dumps(telemetry_dict)

        self.db_cursor.execute(
            "insert into telemetry values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                telemetry_type,
                category,
                sub_category,
                source_name,
                process_type,
                start_date_time,
                str(run_time_in_seconds),
                telemetry_json,
                traffic_light,
                str(io_time_in_seconds),
            ],
        )

    def select_records(
        self,
        telemetry_type: str,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: str,
        from_date_time: datetime,
        to_date_time: datetime,
    ) -> Iterator:
        """
        Select telemetry records unique to a single process, source category
        and sub category for as specific time period.
        """
        if not self.db_cursor:
            raise exceptions.StorageNotInitialized

        select_statement = (
            "SELECT * FROM telemetry WHERE "
            f"telemetry_type='{telemetry_type}' AND "
            f"category='{category}' AND "
            f"sub_category='{sub_category}' AND "
            f"source_name='{source_name}' AND "
            f"process_type='{process_type}' AND "
            f"start_date_time >= '{from_date_time}' AND "
            f"start_date_time < '{to_date_time}'"
        )

        return self.db_cursor.execute(select_statement)

    def _remove_existing_aggregation_telemetry(self, telemetry: TelemetryModel) -> None:
        """
        Removes any already existing aggregations for a specific telemetry
        aggregation.
        If you want to run and store a new aggregation object (for example a
        daily aggrgation) then the already daily aggregation for that day must
        be removed.

        Args:
            telemetry (TelemetryModel): The new telemetry aggregation object
        """
        query_params_exist_aggr = self._get_aggr_telem_query_params(telemetry)
        self.delete_records(**query_params_exist_aggr)

    def delete_records(
        self,
        telemetry_type: str,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: str,
        from_date_time: datetime,
        to_date_time: datetime,
    ) -> None:
        """
        Delete telemetry records unique to a single process, source category
        and sub category for as specific time period.
        """
        if not self.db_cursor:
            raise exceptions.StorageNotInitialized

        select_statement = (
            "DELETE * FROM telemetry WHERE "
            f"telemetry_type='{telemetry_type}' AND "
            f"category='{category}' AND "
            f"sub_category='{sub_category}' AND "
            f"source_name='{source_name}' AND "
            f"process_type='{process_type}' AND "
            f"start_date_time > '{from_date_time}' AND "
            f"start_date_time < '{to_date_time}'"
        )

        self.db_cursor.execute(select_statement)
