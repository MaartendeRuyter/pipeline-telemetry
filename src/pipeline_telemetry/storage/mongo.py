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
from mongoengine import DictField, Document, StringField, connect

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
    start_date_time = StringField()
    run_time_in_seconds = StringField()
    telemetry = DictField(default=None)

    meta = {
        "db_alias": "telemetry",
        "indexes": [
            "category",
            "sub_category",
            "source_name",
            ("category", "sub_category", "source_name", "process_type"),
            "process_type",
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
        category = telemetry_copy.pop("category", None)
        sub_category = telemetry_copy.pop("sub_category", None)
        source_name = telemetry_copy.pop("source_name", None)
        process_type = telemetry_copy.pop("process_type", None)
        start_date_time = telemetry_copy.pop("start_date_time", None)
        run_time_in_seconds = telemetry_copy.pop("run_time_in_seconds", None)
        return {
            "category": category,
            "sub_category": sub_category,
            "source_name": source_name,
            "process_type": process_type,
            "start_date_time": start_date_time,
            "run_time_in_seconds": run_time_in_seconds,
            "telemetry": telemetry_copy,
        }
