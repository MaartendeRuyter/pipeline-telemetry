"""
Helper methods provide date range iterarors.

These date ranges are to be used in TelemetryStorage queries used
by the TelemetryAggregator classes.

The date range includes start_date and end_date to be used in the query.

generic methods:

- date_range_generator
        generic generator, not likely to be used outside this module

Single day date range generators.
- get_daily_date_ranges: free choice of start and end date
- get_daily_date_range_till_yesterday: from start date till yesterday
- get_daily_date_range_yesterday: date range for yesterday


"""

from datetime import datetime
from typing import NamedTuple, Protocol

from pipeline_telemetry.data_classes import TelemetryModel


class TelemetrySelector(NamedTuple):
    """Named tuple to define mandatory attributed for a Telemetry selection.

    This object should be used as input to the Telemetry Aggregator

    >>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
    >>> aggregator = AggregatorClass(
            telemetry_selector=telemetry_selector,
            telemetry_storage=TelemetryStorageClass()
        )

    The `telemtry_selector` defines what telemetry objects are in scope.
    The `aggregator` object defines what kind of aggregation is done (by
    selecting the AggregatorClass) and provides you with metods to run the
    aggergation for a specific period.
    """

    category: str
    sub_category: str
    source_name: str
    process_type: str


class TelemetryListArgs(NamedTuple):
    telemetry_type: str
    category: str
    sub_category: str
    source_name: str
    process_type: str
    from_date_time: datetime
    to_date_time: datetime


class TelemetryList(Protocol):
    def __next__(self) -> TelemetryModel: ...

    def __iter__(self) -> "TelemetryList": ...


class TelemetryAggregator:
    __telemetry: TelemetryModel

    def __init__(self, telemetry: TelemetryModel) -> None:
        self.__telemetry = telemetry

    def aggregate(self, telemetry_list: TelemetryList) -> TelemetryModel:
        for telemetry in telemetry_list:
            self.__telemetry += telemetry
        return self.__telemetry
