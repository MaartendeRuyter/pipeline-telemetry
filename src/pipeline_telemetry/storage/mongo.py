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

from datetime import datetime
from typing import Any, Dict, Iterator

from mongoengine import (
    DateTimeField,
    DictField,
    Document,
    FloatField,
    StringField,
    connect,
)

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

    def to_dict(self) -> Dict:
        """
        Method to convert TelemetryMongoModel instance to a dict that can be
        used to instatiate a TelemetryModel object.
        The mongo object '_id' field needs to be removed as it is not used by
        TelemetryModel.
        """
        telemetry_dict = self.to_mongo().to_dict()
        telemetry_dict.pop("_id", None)
        # run_time_on_seconds is stored as str in Mongo but needs to be a float
        # when processing telemetry data
        telemetry_dict[st.RUN_TIME] = float(telemetry_dict[st.RUN_TIME])
        return telemetry_dict


class TelemetryMongoStorage(AbstractTelemetryStorage):
    """
    Class to provice telemetry in mongo storage class.
    This class can be used as storage_class argument when creating
    an instance of Telemetry.
    """

    def store_aggregated_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        self._remove_existing_aggregation_telemetry(telemetry)
        self.store_telemetry(telemetry)

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        telemetry_mongo_kwargs = self._telemetry_model_kwargs(telemetry)
        TelemetryMongoModel(**telemetry_mongo_kwargs).save()

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
        for telemetry_inst in self.select_records(**query_params_exist_aggr):
            telemetry_inst.delete()

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
            k: v.__dict__ for k, v in getattr(telemetry, st.TELEMETRY_FIELD_KEY).items()
        }

        return {
            st.TELEMETRY_TYPE_KEY: telemetry_type,
            st.CATEGORY_KEY: category,
            st.SUB_CATEGORY_KEY: sub_category,
            st.SOURCE_NAME_KEY: source_name,
            st.PROCESS_TYPE_KEY: process_type,
            st.START_TIME: start_date_time,
            st.RUN_TIME: str(round(run_time_in_seconds, 2)),
            st.TRAFFIC_LIGHT_KEY: traffic_light,
            st.TELEMETRY_FIELD_KEY: telemetry_data,
            st.IO_TIME_KEY: io_time_in_seconds,
        }

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
        query_details = {
            "telemetry_type": telemetry_type,
            "category": category,
            "sub_category": sub_category,
            "source_name": source_name,
            "process_type": process_type,
        }

        return TelemetryMongoModel.objects(
            start_date_time__gte=from_date_time,
            start_date_time__lt=to_date_time,
            **query_details,
        )

    @staticmethod
    def _db_object_to_dict(db_object: Any) -> Dict:
        """Returns a db object as a dict object."""
        # Mongo onbject need to be converted to Dict object first
        return db_object.to_dict()
