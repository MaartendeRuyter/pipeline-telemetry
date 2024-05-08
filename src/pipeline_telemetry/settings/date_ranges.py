""" """

from datetime import date, datetime, timedelta
from typing import Iterator, NamedTuple


class DateRange(NamedTuple):
    from_date: date
    to_date: date


class DateTimeRange(NamedTuple):
    from_date: datetime
    to_date: datetime


def date_range_to_date_time_range(date_range: DateRange) -> DateTimeRange:
    start_date, end_date = date_range
    start_date_time = datetime(*start_date.timetuple()[:6])
    end_date_time = datetime(*end_date.timetuple()[:6])
    return DateTimeRange(start_date_time, end_date_time)


def date_range_generator(
    start_date_time: datetime, end_date_time: datetime, time_delta: timedelta
) -> Iterator[DateTimeRange]:
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
        yield date_range_to_date_time_range(DateRange(start_date, end_date))
        start_date, end_date = end_date, end_date + time_delta


def get_daily_date_ranges(start_date: date, end_date: date) -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges from start_date to end_date.
    """
    start_date_time = datetime(*start_date.timetuple()[:6])
    end_date_time = datetime(*end_date.timetuple()[:6])
    return date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=timedelta(days=1),
    )


def get_daily_date_range_till_yesterday(start_date: date) -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges from start_date till yesterday.
    """
    end_date = date.today()
    return get_daily_date_ranges(start_date=start_date, end_date=end_date)


def get_daily_date_range_yesterday() -> Iterator[DateTimeRange]:
    """
    Iterator to return single day date ranges for yesterday.
    """
    end_date = date.today()
    start_date = date.today() - timedelta(days=1)
    return get_daily_date_ranges(start_date=start_date, end_date=end_date)


def get_daily_date_range_for_single_date(date: date) -> DateTimeRange:
    """
    Return single daily date range for a given date.
    """
    return next(
        get_daily_date_ranges(start_date=date, end_date=date + timedelta(days=1))
    )


def get_monthly_date_range_for_single_date(date: date) -> DateTimeRange:
    """
    Return single monthly date range for a given date.
    """
    first_day_of_month = date.replace(day=1)
    first_day_next_month = (date.replace(day=1) + timedelta(days=32)).replace(day=1)
    return date_range_to_date_time_range(
        DateRange(from_date=first_day_of_month, to_date=first_day_next_month)
    )


def get_weekly_date_range_for_single_date(date: date) -> DateTimeRange:
    """
    Return single weekly date range for a given date.
    """
    first_day_of_week = date - timedelta(days=date.weekday())
    first_day_next_week = first_day_of_week + timedelta(days=7)
    return date_range_to_date_time_range(
        DateRange(from_date=first_day_of_week, to_date=first_day_next_week)
    )
