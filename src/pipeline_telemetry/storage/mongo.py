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

from ..data_classes import TelemetryModel
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

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        telemetry_mongo_kwargs = self._telemetry_model_kwargs(telemetry)
        TelemetryMongoModel(**telemetry_mongo_kwargs).save()

    @staticmethod
    def _telemetry_model_kwargs(telemetry: TelemetryModel) -> dict:
        """
        Returns a dicts with kwargs that can be used to create a new
        TelemetryMongoStorage instance.
        """
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

        return {
            st.TELEMETRY_TYPE_KEY: telemetry_type,
            st.CATEGORY_KEY: category,
            st.SUB_CATEGORY_KEY: sub_category,
            st.SOURCE_NAME_KEY: source_name,
            st.PROCESS_TYPE_KEY: process_type,
            st.START_TIME: start_date_time,
            st.RUN_TIME: run_time_in_seconds,
            st.TRAFFIC_LIGHT_KEY: traffic_light,
            st.TELEMETRY_FIELD_KEY: telemetry_data,
            st.IO_TIME_KEY: io_time_in_seconds,
        }
