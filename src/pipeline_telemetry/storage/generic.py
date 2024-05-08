"""Module to define abstract storage class"""

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Any, Dict, Iterator, TypedDict

from ..data_classes import TelemetryData, TelemetryModel
from ..settings import (
    AGGR_DATE_TIME_RANGE_METHODS,
    CATEGORY_KEY,
    PROCESS_TYPE_KEY,
    SOURCE_NAME_KEY,
    START_TIME,
    SUB_CATEGORY_KEY,
    TELEMETRY_TYPE_KEY,
)
from ..settings.date_ranges import DateTimeRange
from ..settings.exceptions import RequestedDataTimeRangeMethodNotFound


class UniqueAggregatedTelemetryKeys(TypedDict):
    """
    Class to define what query params are needed to define a unique
    aggregated telemetry object. For a set of query params given only 0 or 1
    telemetry object is allowed to exist (i.e. a daily aggregation can only
    occur once for each day, a weekly aggregation only once for each weak etc.)
    """

    telemetry_type: str
    category: str
    sub_category: str
    source_name: str
    process_type: str
    from_date_time: datetime
    to_date_time: datetime


class AbstractTelemetryStorage(metaclass=ABCMeta):
    """Abstract Telemetry Storage class

    implements store_telemetry method that persists a given telemetry object

    Any class that stores the telemetry objects should be subclassed from
    this Abstract Class
    """

    __TELEMETRY_KEY: str = "telemetry"

    @abstractmethod
    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""

    @abstractmethod
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
        Select telemetry records unique to a single process and source for as specific time period.
        """

    @abstractmethod
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

    def _telemetry_storage_to_object(
        self, stored_telemetry_object: Dict
    ) -> TelemetryModel:
        """Method to convert a sql light object into"""
        telemetry_data = stored_telemetry_object.pop(self.__TELEMETRY_KEY, "{}")
        telemetry_model = TelemetryModel(**stored_telemetry_object)
        for sub_process, sub_process_tel_data in telemetry_data.items():
            telemetry_model.telemetry.update(
                {sub_process: TelemetryData(**sub_process_tel_data)}
            )
        return telemetry_model

    @staticmethod
    def _db_object_to_dict(db_object: Any) -> Dict:
        """Returns a db object as a dict object."""
        # If the persistance model does not return a proper Dict object then
        # override this method to ensure a Dict object is available.
        return db_object

    def _get_aggr_telem_query_params(
        self, telemetry: TelemetryModel
    ) -> UniqueAggregatedTelemetryKeys:
        """
        Returns a dict with the query params to retrieve a unique aggregated
        telemetry object.

        Args:
            telemetry (TelemetryModel): The new telemetry aggregation object

        returns:
            UniqueAggregatedTelemetryKeys:
                TypedDict with query params that can be used as input for a
                DB query to retrieve all instances of unique aggregated
                telemetry object (should in theory always return 0 or 1
                instance.
        """
        date_time_range = self._get_aggr_telem_date_time_range(telemetry)
        return UniqueAggregatedTelemetryKeys(
            telemetry_type=getattr(telemetry, TELEMETRY_TYPE_KEY),
            source_name=getattr(telemetry, SOURCE_NAME_KEY),
            category=getattr(telemetry, CATEGORY_KEY),
            sub_category=getattr(telemetry, SUB_CATEGORY_KEY),
            process_type=getattr(telemetry, PROCESS_TYPE_KEY),
            from_date_time=date_time_range.from_date,
            to_date_time=date_time_range.to_date,
        )

    @staticmethod
    def _get_aggr_telem_date_time_range(telemetry: TelemetryModel) -> DateTimeRange:
        """
        Method to get the correct datatime range for a date depending on the
        aggregation telemetry_type.
        For example for a monthly aggregation the input date of 2022-10-10
        will be converted into a datetime range of (2022-10-01, 2022-11-01).
        For a daily aggegration this would result in (2022-10-10, 2022-10-11).
        etc.
        """
        start_date_time = getattr(telemetry, START_TIME)
        telemetry_type = getattr(telemetry, TELEMETRY_TYPE_KEY)
        date_time_range_method = AGGR_DATE_TIME_RANGE_METHODS.get(telemetry_type)
        if not date_time_range_method:
            raise RequestedDataTimeRangeMethodNotFound(telemetry_type)

        return date_time_range_method(start_date_time.date())

    def telemetry_list(
        self,
        telemetry_type: str,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: str,
        from_date_time: datetime,
        to_date_time: datetime,
    ) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved
        from a database query with the provided arguments.
        """
        selected_records = self.select_records(
            telemetry_type=telemetry_type,
            category=category,
            sub_category=sub_category,
            source_name=source_name,
            process_type=process_type,
            from_date_time=from_date_time,
            to_date_time=to_date_time,
        )
        for record in selected_records:
            record_dict = self._db_object_to_dict(record)
            yield self._telemetry_storage_to_object(record_dict)
