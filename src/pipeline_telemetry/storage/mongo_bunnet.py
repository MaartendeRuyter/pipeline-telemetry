"""Module to provide a storage class for using Bunnet."""

from datetime import datetime
from typing import Annotated, Iterator, Optional, Sequence, Type

from bunnet import Document, Indexed, init_bunnet
from pymongo import MongoClient

from ..data_classes import TelemetryModel
from ..settings import settings as st
from .generic import AbstractTelemetryStorage

DEFAULT_DB_NAME = "GeoDataGardenTelemetry"
DEFAULT_DB_ALIAS = "geo_datagarden"


class TelemetryBunnetModel(Document):
    """
    Class to provice telemetry Mongo Model for persistance in MongoDB using Bunnet.
    """

    category: Annotated[str, Indexed()]
    sub_category: Annotated[str, Indexed()]
    source_name: Annotated[str, Indexed()]
    process_type: Annotated[str, Indexed()]
    start_date_time: Annotated[datetime, Indexed()]
    run_time_in_seconds: str
    traffic_light: Annotated[str, Indexed()]
    telemetry_type: str
    io_time_in_seconds: float = 0
    telemetry: Optional[dict] = None

    # meta = {
    #     "db_alias": "telemetry",
    #     "indexes": [
    #         "category",
    #         "sub_category",
    #         "source_name",
    #         ("category", "sub_category", "source_name", "process_type"),
    #         "process_type",
    #         "traffic_light",
    #         "start_date_time",
    #     ],
    # }

    def to_dict(self) -> dict:
        """
        Method to convert TelemetryMongoModel instance to a dict that can be
        used to instatiate a TelemetryModel object.
        The mongo object '_id' field needs to be removed as it is not used by
        TelemetryModel.
        """
        telemetry_dict = self.model_dump()
        telemetry_dict.pop("_id", None)
        # run_time_on_seconds is stored as str in Mongo but needs to be a float
        # when processing telemetry data
        telemetry_dict[st.RUN_TIME] = float(telemetry_dict[st.RUN_TIME])
        return telemetry_dict


class TelemetryBunnetStorage(AbstractTelemetryStorage):
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
        TelemetryBunnetModel(**telemetry_mongo_kwargs).save()  # type: ignore

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

        return TelemetryBunnetModel.objects(
            start_date_time__gte=from_date_time,
            start_date_time__lt=to_date_time,
            **query_details,
        )

    @staticmethod
    def _db_object_to_dict(db_object: Document) -> dict:
        """Returns a db object as a dict object."""
        # Mongo onbject need to be converted to Dict object first
        return db_object.model_dump()


ALL_MODEL_CLASSES: Sequence[Type[Document]] = [TelemetryBunnetModel]


def init_database(
    db_url: str = "mongodb://localhost:27017",
    db: Optional[str] = DEFAULT_DB_NAME,
    alias: str = DEFAULT_DB_ALIAS,
    document_models: Optional[Sequence[Type[Document]]] = None,
    **kwargs,
):
    """
    Allows users to configure the database connection.

    Parameters:
    - alias (str): The connection alias.
    - kwargs: Additional keyword arguments supported by mongoengine.connect().
    """
    # Bunnet uses Pymongo client under the hood
    client: MongoClient = MongoClient(db_url)
    # Initialize bunnet with the Product document class
    init_bunnet(
        database=client.db_name,
        document_models=document_models or ALL_MODEL_CLASSES,  # type: ignore
    )
