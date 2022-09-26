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
from datetime import datetime
from typing import Dict, Iterator, NamedTuple, Protocol, Union

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import settings as st

from .helper import DateTimeRange


class TelemetrySelector(NamedTuple):
    category: str
    sub_category: str
    source_name: str
    process_type: str


class TelemetryList(Protocol):

    def telemetry_list(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database query with the provided arguments.
        """
        ... 

class TelemetryProtocol(Protocol):
    """For the purpose of the TelemetryAggregator adddimg all the new telemetry needs to be able to ad"""

    def __add__(self, telemetry: 'TelemetryProtocol') -> 'TelemetryProtocol':
        ...


class TelemetryList(Protocol):
    def __next__(self) -> TelemetryProtocol:
        ...

    def __iter__(self) -> 'TelemetryList':
        ...


class TelemetryAggregator():

    __telemetry: TelemetryProtocol

    def __init__(self, telemetry: TelemetryProtocol) -> None:
        self.__telemetry = telemetry

    def aggregate_from(
            self, telemetry_list: TelemetryList) -> TelemetryProtocol:
        for telemetry in telemetry_list:
            self.__telemetry += telemetry
        return self.__telemetry


class DailyAggregator():

    FROM_TELEMETRY_TYPE = st.SINGLE_TELEMETRY_TYPE
    TO_TELEMETRY_TYPE = st.DAILY_AGGR_TELEMETRY_TYPE

    __telemetry_selector: TelemetrySelector
    __target_telemetry_model: TelemetryModel
    __telemetry_storage: TelemetryList

    def __init__(
            self, telemetry_selector: TelemetrySelector,
            telemetry_storage: TelemetryList) -> None:
        self.__telemetry_selector = telemetry_selector
        self.__telemetry_storage = telemetry_storage
        self._set_target_telemetry_model()

    @property
    def target_telemetry_model(self):
        return self.__target_telemetry_model    

    def _set_target_telemetry_model(self):
        target_telem_params = self.__telemetry_selector._asdict() | \
            {'telemetry_type': self.TO_TELEMETRY_TYPE}

        self.__target_telemetry_model = TelemetryModel(**target_telem_params)

    def _storage_query_params(
            self, date_time_range: DateTimeRange
    ) -> Dict[str, Union[str, datetime]]:
        storage_q_params = \
            self.__telemetry_selector.__dict__ | \
            {'telemetry_type': self.FROM_TELEMETRY_TYPE}

        return
