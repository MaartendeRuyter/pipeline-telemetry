"""Module to provide a storage class for using MongoDB.

When using MongoDB storage class you can select the mongoDB instance to be used
via environment Variables

MONGO_DB_NAME (defaults to `telemetry`)
MONGO_DB_PASSWORD
MONGO_DB_USERNAME
MONGO_DB_HOST
MONGO_DB_PORT

If no host and port are defined the connection will dedault to a localhost
mongoDB instance.
"""
from mongoengine import DateTimeField, DictField, Document, FloatField, \
    StringField, connect

from ..settings import settings as st
from .generic import AbstractTelemetryStorage
from .mongo_connection import MONGO_ACCESS_PARAMS

connect(alias="telemetry", **MONGO_ACCESS_PARAMS)


class TelemetryMongoModel(Document):
    """
    Class to provice telemetry Mongo Model for persistance in MongoDB
    """

    category = StringField()
    sub_category = StringField()
    source_name = StringField()
    process_type = StringField()
    start_date_time = DateTimeField()
    run_time_in_seconds = StringField()
    traffic_light = StringField()
    telemetry_type = StringField()
    io_time_in_seconds = FloatField(default=0)
    telemetry = DictField(default=None)

    meta = {
        "db_alias": "telemetry",
        "indexes": [
            "category",
            "sub_category",
            "source_name",
            ("category", "sub_category", "source_name", "process_type"),
            "process_type",
            "traffic_light",
            "start_date_time",
        ],
    }


class TelemetryMongoStorage(AbstractTelemetryStorage):
    """
    Class to provice telemetry in mongo storage class.
    This class can be used as storage_class argument when creating
    an instance of Telemetry.
    """

    def store_telemetry(self, telemetry: dict) -> None:
        """public method to persist telemetry object"""
        telemetry_mongo_kwargs = self._telemetry_model_kwargs(telemetry)
        TelemetryMongoModel(**telemetry_mongo_kwargs).save()

    @staticmethod
    def _telemetry_model_kwargs(telemetry: dict) -> dict:
        """
        Returns a dicts with kwargs that can be used to create a new
        TelemetryMongoStorage instance.
        """
        telemetry_copy = telemetry.copy()
        telemetry_type = telemetry_copy.pop(st.TELEMETRY_TYPE_KEY, None)
        category = telemetry_copy.pop(st.CATEGORY_KEY, None)
        sub_category = telemetry_copy.pop(st.SUB_CATEGORY_KEY, None)
        source_name = telemetry_copy.pop(st.SOURCE_NAME_KEY, None)
        process_type = telemetry_copy.pop(st.PROCESS_TYPE_KEY, None)
        start_date_time = telemetry_copy.pop(st.START_TIME, None)
        run_time_in_seconds = telemetry_copy.pop(st.RUN_TIME, None)
        traffic_light = telemetry_copy.pop(st.TRAFFIC_LIGHT_KEY, None)
        io_time_in_seconds = telemetry_copy.pop(st.IO_TIME_KEY, None)

        return {
            st.TELEMETRY_TYPE_KEY: telemetry_type,
            st.CATEGORY_KEY: category,
            st.SUB_CATEGORY_KEY: sub_category,
            st.SOURCE_NAME_KEY: source_name,
            st.PROCESS_TYPE_KEY: process_type,
            st.START_TIME: start_date_time,
            st.RUN_TIME: run_time_in_seconds,
            st.TRAFFIC_LIGHT_KEY: traffic_light,
            st.TELEMETRY_FIELD_KEY: telemetry_copy,
            st.IO_TIME_KEY: io_time_in_seconds,
        }
