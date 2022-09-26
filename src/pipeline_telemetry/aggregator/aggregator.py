"""
Module to define a the TelemetryAggregator class.

This class creates makes an aggregation from a queryset of telemetry objects.
The aggregation of is added to a telemetry object that is provide to aggregate method of the class instance.

Usage


>>> # create new telemetry object
>>> telemetry_object = Telemetry(**telemtry_params)
>>> # create aggregator
>>> aggregator = TelemetryAggregator(telemetry_object)
>>> # aggregate a telemetry queryset and return the result
>>> aggregated_telemetry = aggregator.aggregate_from(telemetry_queryset)

"""
from datetime import date, datetime
from typing import Dict, Iterator, List, NamedTuple, Protocol, Type, Union

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import settings as st

from .helper import DateTimeRange, get_daily_date_ranges


class TelemetrySelector(NamedTuple):
    category: str
    sub_category: str
    source_name: str
    process_type: str


class TelemetryStorage(Protocol):

    def telemetry_list(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database query with the provided arguments.
        """
        ...

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """ public method to persist telemetry object"""
        ...


class TelemetryList(Protocol):
    def __next__(self) -> TelemetryModel:
        ...

    def __iter__(self) -> 'TelemetryList':
        ...


class TelemetryAggregator():

    __telemetry: TelemetryModel

    def __init__(self, telemetry: TelemetryModel) -> None:
        self.__telemetry = telemetry

    def aggregate(
            self, telemetry_list: TelemetryList) -> TelemetryModel:
        for telemetry in telemetry_list:
            self.__telemetry += telemetry
        return self.__telemetry


class DailyAggregator():

    FROM_TELEMETRY_TYPE = st.SINGLE_TELEMETRY_TYPE
    TO_TELEMETRY_TYPE = st.DAILY_AGGR_TELEMETRY_TYPE

    __telemetry_selector: TelemetrySelector
    __target_telemetry: TelemetryModel
    __telemetry_storage: TelemetryStorage
    __aggregator: Type[TelemetryAggregator] = TelemetryAggregator

    def __init__(
            self, telemetry_selector: TelemetrySelector,
            telemetry_storage: TelemetryStorage) -> None:
        self.__telemetry_selector = telemetry_selector
        self.__telemetry_storage = telemetry_storage
        self._set_target_telemetry_model()

    @property
    def target_telemetry(self):
        return self.__target_telemetry

    def aggregate(self, start_date: date, end_date: date) -> None:
        """Method to run all aggregations in the given time period.
        """
        date_time_ranges = self._get_date_ranges(
            start_date=start_date, end_date=end_date)
        for date_time_range in date_time_ranges:
            aggregated_telemetry = self._run_aggregation(date_time_range)
            self.__telemetry_storage.store_telemetry(aggregated_telemetry)

    def _get_date_ranges(
            self, start_date: date, end_date: date) -> List[DateTimeRange]:
        """
        Method to return the list of date ranges based upon start and end
        date.
        """
        return get_daily_date_ranges(
            start_date=start_date, end_date=end_date)

    def _run_aggregation(
            self, date_time_range: DateTimeRange) -> TelemetryModel:
        """
        Method to run the actual aggregation and return the aggregated telemetry model.
        """
        telemetry_list_params = \
            self._telememtry_list_params(date_time_range)
        telemety_objects = self.__telemetry_storage.telemetry_list(
            **telemetry_list_params)

        return self.__aggregator(
            self.__target_telemetry.copy()).aggregate(telemety_objects)

    def _set_target_telemetry_model(self):
        target_telem_params = self.__telemetry_selector._asdict() | \
            {'telemetry_type': self.TO_TELEMETRY_TYPE}

        self.__target_telemetry = TelemetryModel(**target_telem_params)

    def _telememtry_list_params(self, date_time_range: DateTimeRange) \
            -> Dict[str, Union[str, datetime]]:
        """
        Method to return telemetry_list_params that can be used to retrieve a
        list of TelemetryModel objects from the storage model.

        i.e. these params serve as input to the telemetry_list method of the
        storage_class
        """
        telemetry_list_params = \
            self.__telemetry_selector._asdict() | \
            {'telemetry_type': self.FROM_TELEMETRY_TYPE}
        telemetry_list_params.update(
            from_date_time=date_time_range.from_date,
            to_date_time=date_time_range.to_date)
        return telemetry_list_params
