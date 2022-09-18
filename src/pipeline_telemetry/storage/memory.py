"""[summary]
"""
import json
import sqlite3
from datetime import datetime
from typing import Dict, Iterator, Optional

from pipeline_telemetry.data_classes.telemetry_models import TelemetryData

from ..data_classes import TelemetryModel
from ..settings import exceptions
from ..settings import settings as st
from .generic import AbstractTelemetryStorage


def dict_factory(cursor, row):
    """Method to allow sql queries to be returned as a dict.

    The telemetry_data field is seperately converted to a dict because
    sqlite returns a nested dict as a string.
    """
    col_names = [col[0] for col in cursor.description]
    telemetry_data = {key: value for key, value in zip(col_names, row)}
    telemetry_data_str = telemetry_data.pop('telemetry_data', "{}")
    telemetry_data.update({'telemetry_data': json.loads(telemetry_data_str)})
    return telemetry_data


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
            telemetry_data json, traffic_light varchar(10),
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
        start_date_time = getattr(telemetry, st.START_TIME)
        run_time_in_seconds = getattr(telemetry, st.RUN_TIME)
        traffic_light = getattr(telemetry, st.TRAFFIC_LIGHT_KEY)
        io_time_in_seconds = getattr(telemetry, st.IO_TIME_KEY)
        telemetry_data = {
            k: v.__dict__ for k, v in
            getattr(telemetry, st.TELEMETRY_FIELD_KEY).items()
        }
        json_object = json.dumps(telemetry_data)

        self.db_cursor.execute(
            "insert into telemetry values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                telemetry_type, category, sub_category,
                source_name, process_type, start_date_time,
                str(run_time_in_seconds), json_object,
                traffic_light, str(io_time_in_seconds)
            ])

    def select_records(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator:
        """
        Select telemetry records unique to a single process, source category
        and sub category for as specific time period.
        """
        if not self.db_cursor:
            raise exceptions.StorageNotInitialized

        select_statement = \
            ("SELECT * FROM telemetry WHERE "
             f"telemetry_type='{telemetry_type}' AND "
             f"category='{category}' AND "
             f"sub_category='{sub_category}' AND "
             f"source_name='{source_name}' AND "
             f"process_type='{process_type}' AND "
             f"start_date_time > '{from_date_time}' AND "
             f"start_date_time < '{to_date_time}'")

        return self.db_cursor.execute(select_statement)

    @staticmethod
    def _telemetry_storage_to_object(
            stored_telemetry_object: Dict) -> TelemetryModel:
        """Method to convert a sql light object into """
        telemetry_data = stored_telemetry_object.pop('telemetry_data', "{}")
        telemetry_model = TelemetryModel(**stored_telemetry_object)
        for sub_process, sub_process_tel_data in telemetry_data.items():
            telemetry_model.telemetry.update(
                {sub_process: TelemetryData(**sub_process_tel_data)}
            )

        return telemetry_model

    def telemetry_list(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database query with the provided arguments.
        """
        selected_records = self.select_records(
            telemetry_type=telemetry_type, category=category,
            sub_category=sub_category, source_name=source_name,
            process_type=process_type, from_date_time=from_date_time,
            to_date_time=to_date_time
        )
        for record in selected_records:
            yield self._telemetry_storage_to_object(record)
