"""Module for testing date_ranges functions."""

from datetime import date, datetime, timedelta

from pipeline_telemetry.settings.date_ranges import (
    DateTimeRange,
    date_range_generator,
    get_daily_date_range_for_single_date,
    get_daily_date_range_till_yesterday,
    get_daily_date_range_yesterday,
    get_daily_date_ranges,
    get_monthly_date_range_for_single_date,
    get_weekly_date_range_for_single_date,
)


def str_to_date_time(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def str_to_date(date_str: str) -> date:
    return str_to_date_time(date_str).date()


def test_date_range_generator():
    """Test date_range_generator generates DateTimeRanges."""
    start_date_time = datetime.strptime("2022-01-18", "%Y-%m-%d")
    time_delta = timedelta(days=1)
    end_date_time = start_date_time + timedelta(days=3)
    daterange_generator = date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=time_delta,
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(str_to_date_time("2022-01-18"), str_to_date_time("2022-01-19")),
        DateTimeRange(str_to_date_time("2022-01-19"), str_to_date_time("2022-01-20")),
        DateTimeRange(str_to_date_time("2022-01-20"), str_to_date_time("2022-01-21")),
    ]


def test_date_range_generator_with_during_day_time_stamps():
    """
    Test date_range_generator generates correct DateTimeRanges when atributes
    contain a time other the 00:00:00. The first daterange should start with
    the date part of the from_data."""
    start_date_time = datetime.strptime("2022-01-18 13:55:26", "%Y-%m-%d %H:%M:%S")
    time_delta = timedelta(days=1)
    end_date_time = start_date_time + timedelta(days=3)
    daterange_generator = date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=time_delta,
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(str_to_date_time("2022-01-18"), str_to_date_time("2022-01-19")),
        DateTimeRange(str_to_date_time("2022-01-19"), str_to_date_time("2022-01-20")),
        DateTimeRange(str_to_date_time("2022-01-20"), str_to_date_time("2022-01-21")),
    ]


def test_get_daily_date_ranges():
    """Test daterange_generator returns DateTimeRange ranges."""
    start_date = date(year=2022, month=1, day=18)
    end_date = date(year=2022, month=1, day=21)
    daterange_generator = get_daily_date_ranges(
        start_date=start_date, end_date=end_date
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(str_to_date_time("2022-01-18"), str_to_date_time("2022-01-19")),
        DateTimeRange(str_to_date_time("2022-01-19"), str_to_date_time("2022-01-20")),
        DateTimeRange(str_to_date_time("2022-01-20"), str_to_date_time("2022-01-21")),
    ]


def test_get_daily_date_range_till_yesterday():
    """
    Test get_daily_date_range_till_yesterday generates a DateTimeRange
    till yesterday.
    """
    start_date = date.today() - timedelta(days=3)
    daterange_generator = get_daily_date_range_till_yesterday(start_date=start_date)
    result = [daterange for daterange in daterange_generator]
    assert len(result) == 3


def test_get_daily_date_ranges_yesterday():
    """
    Test get_daily_date_ranges_yesterday generates a DateTimeRange
    for only yesterday.
    """
    today = datetime.strftime(datetime.now(), "%Y-%m-%d")
    yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")

    daterange_generator = get_daily_date_range_yesterday()
    result = [daterange for daterange in daterange_generator]
    assert result[0].from_date == str_to_date_time(yesterday)
    assert result[0].to_date == str_to_date_time(today)
    assert len(result) == 1


def test_get_daily_date_range_for_single_date():
    """
    Test get_daily_date_range_for_single_date returns a single DateTimeRange.
    """
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    single_daily_date_range = get_daily_date_range_for_single_date(date=yesterday)

    assert isinstance(single_daily_date_range, DateTimeRange)
    assert single_daily_date_range.from_date.date() == yesterday
    assert single_daily_date_range.to_date.date() == today


def test_get_monthly_date_range_for_single_date():
    """
    Test get_monthly_date_range_for_single_date returns a single DateTimeRange.
    """
    first_day_of_month = datetime.strptime("2022-02-01", "%Y-%m-%d")
    first_day_of_next_month = datetime.strptime("2022-03-01", "%Y-%m-%d")
    input_date = datetime.strptime("2022-02-11", "%Y-%m-%d")
    single_monthly_date_range = get_monthly_date_range_for_single_date(date=input_date)
    assert isinstance(single_monthly_date_range, DateTimeRange)
    assert single_monthly_date_range.from_date == first_day_of_month
    assert single_monthly_date_range.to_date == first_day_of_next_month


def test_get_weekly_date_range_for_single_date():
    """
    Test get_monthly_date_range_for_single_date returns a single DateTimeRange.
    """
    first_day_of_week = datetime.strptime("2022-10-03", "%Y-%m-%d")
    first_day_of_next_week = datetime.strptime("2022-10-10", "%Y-%m-%d")
    input_date = datetime.strptime("2022-10-07", "%Y-%m-%d")
    single_weekly_date_range = get_weekly_date_range_for_single_date(
        date=input_date.date()
    )
    assert isinstance(single_weekly_date_range, DateTimeRange)
    assert single_weekly_date_range.from_date == first_day_of_week
    assert single_weekly_date_range.to_date == first_day_of_next_week
