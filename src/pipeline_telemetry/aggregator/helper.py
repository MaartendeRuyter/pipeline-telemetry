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
from datetime import date, datetime, timedelta
from typing import Iterator, NamedTuple, Protocol

from pipeline_telemetry.data_classes import TelemetryModel


class TelemetrySelector(NamedTuple):
    """Named tuple to define mandatory attributed for a Telemetry selection.

    This object should be used as input to the Telemetry Aggregator

    >>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
    >>> aggeregator = AggregatorClass(
            telemetry_selector=telemetry_selector,
            telemetry_storage=TelemetryStorageClass()
        )
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


class DateRange(NamedTuple):
    from_date: date
    to_date: date


class DateTimeRange(NamedTuple):
    from_date: datetime
    to_date: datetime


def date_range_to_date_time_range(
        date_range: DateRange) -> DateTimeRange:
    start_date, end_date = date_range
    start_date_time = datetime(*start_date.timetuple()[:6])
    end_date_time = datetime(*end_date.timetuple()[:6])
    return DateTimeRange(start_date_time, end_date_time)


def date_range_generator(
        start_date_time: datetime,
        end_date_time: datetime,
        time_delta: timedelta) -> Iterator[DateTimeRange]:
    """Iterator for a list of DateTimeRange object

    Args:
        start_date_time (datetime): start date
        end_date_time (datetime): end date
        time_delta (timedelta): lengt of date time range

    The resulting date
    Yields:
        Iterator[DateTimeRange]: _description_
    """
    start_date = start_date_time.date()
    end_date = start_date + time_delta
    while end_date <= end_date_time.date():
        yield date_range_to_date_time_range(
            DateRange(start_date, end_date))
        start_date, end_date = end_date, end_date + time_delta


def get_daily_date_ranges(
        start_date: date, end_date: date) -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges from start_date to end_date.
    """
    start_date_time = datetime(*start_date.timetuple()[:6])
    end_date_time = datetime(*end_date.timetuple()[:6])
    return date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=timedelta(days=1)
    )


def get_daily_date_range_till_yesterday(
        start_date: date) -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges from start_date till yesterday.
    """
    end_date = date.today()
    return get_daily_date_ranges(
        start_date=start_date, end_date=end_date
    )


def get_daily_date_range_yesterday() -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges for yesterday.
    """
    end_date = date.today()
    start_date = date.today() - timedelta(days=1)
    return get_daily_date_ranges(
        start_date=start_date, end_date=end_date
    )
