""" Module for testing aggregator helper functions
"""
from datetime import date, datetime, timedelta

from pipeline_telemetry.aggregator.helper import \
    date_range_generator, DateTimeRange, get_daily_date_ranges, \
    get_daily_date_range_till_yesterday, get_daily_date_range_yesterday


def str_to_date_time(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%d')


def str_to_date(date_str: str) -> date:
    return str_to_date_time(date_str).date()


def test_date_range_generator():
    start_date_time = datetime.strptime("2022-01-18", '%Y-%m-%d')
    time_delta=timedelta(days=1)
    end_date_time = start_date_time + timedelta(days=3)
    daterange_generator = date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=time_delta
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(
            (str_to_date_time('2022-01-18'), str_to_date_time('2022-01-19'))),
        DateTimeRange(
            (str_to_date_time('2022-01-19'), str_to_date_time('2022-01-20'))),
        DateTimeRange(
            (str_to_date_time('2022-01-20'), str_to_date_time('2022-01-21')))]


def test_date_range_generator_with_during_day_time_stamps():
    start_date_time = datetime.strptime(
        "2022-01-18 13:55:26", '%Y-%m-%d %H:%M:%S')
    time_delta=timedelta(days=1)
    end_date_time = start_date_time + timedelta(days=3)
    daterange_generator = date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=time_delta
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(
            (str_to_date_time('2022-01-18'), str_to_date_time('2022-01-19'))),
        DateTimeRange(
            (str_to_date_time('2022-01-19'), str_to_date_time('2022-01-20'))),
        DateTimeRange(
            (str_to_date_time('2022-01-20'), str_to_date_time('2022-01-21')))]



def test_date_range_generator():
    start_date_time = datetime.strptime("2022-01-18", '%Y-%m-%d')
    time_delta=timedelta(days=1)
    end_date_time = start_date_time + timedelta(days=3)
    daterange_generator = date_range_generator(
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        time_delta=time_delta
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(
            (str_to_date_time('2022-01-18'), str_to_date_time('2022-01-19'))),
        DateTimeRange(
            (str_to_date_time('2022-01-19'), str_to_date_time('2022-01-20'))),
        DateTimeRange(
            (str_to_date_time('2022-01-20'), str_to_date_time('2022-01-21')))]


def test_get_daily_date_ranges():
    start_date = date(year=2022, month=1, day=18)
    end_date = date(year=2022, month=1, day=21)
    daterange_generator = get_daily_date_ranges(
        start_date=start_date,
        end_date=end_date
    )
    result = [daterange for daterange in daterange_generator]
    assert result == [
        DateTimeRange(
            (str_to_date_time('2022-01-18'), str_to_date_time('2022-01-19'))),
        DateTimeRange(
            (str_to_date_time('2022-01-19'), str_to_date_time('2022-01-20'))),
        DateTimeRange(
            (str_to_date_time('2022-01-20'), str_to_date_time('2022-01-21')))]


def test_get_daily_date_range_till_yesterday():
    start_date = date.today() - timedelta(days=3)
    daterange_generator = get_daily_date_range_till_yesterday(
        start_date=start_date)
    result = [daterange for daterange in daterange_generator]
    assert len(result) == 3


def test_get_daily_date_ranges_yesterday():
    today = datetime.strftime(datetime.now(), '%Y-%m-%d') 
    yesterday = datetime.strftime(
        datetime.now() - timedelta(days=1), '%Y-%m-%d') 

    daterange_generator = get_daily_date_range_yesterday()
    result = [daterange for daterange in daterange_generator]
    assert result == [DateTimeRange(
        (str_to_date_time(yesterday), str_to_date_time(today)))]
