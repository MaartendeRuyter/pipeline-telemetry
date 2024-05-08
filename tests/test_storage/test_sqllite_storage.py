"""Module to test storage module."""

import sqlite3
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from test_storage_data import DEFAULT_TELEMETRY_MODEL_PARAMS, DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry import Telemetry
from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import DateTimeRange, exceptions
from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.storage.generic import AbstractTelemetryStorage
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage


def telemetry_query_params():
    """Returns a default set of query params"""
    return DEFAULT_TELEMETRY_MODEL_PARAMS | {
        "from_date_time": datetime.now() - timedelta(days=1),
        "to_date_time": datetime.now() + timedelta(days=1),
    }


def test_in_abstract_strorage_class_exists():
    """Test that abstract storage class exists."""
    assert AbstractTelemetryStorage


def test_in_memory_strorage_class_exists():
    """Test that in memory storage class exists."""
    assert TelemetryInMemoryStorage


def test_db_object_to_dict_method():
    """
    Test _db_object_to_dict method exists and if no override is done returns an
    object unchanged.
    """
    in_memory_storage = TelemetryInMemoryStorage()
    assert in_memory_storage._db_object_to_dict({"test": "dict"}) == {"test": "dict"}


def test_get_aggr_telem_query_params():
    """
    Test _get_aggr_telem_query_params converts TelemetryModel into
    dict with the correct keys.
    """
    telemetry_params = DEFAULT_TELEMETRY_MODEL_PARAMS.copy() | {
        "telemetry_type": "DAILY AGGREGATION"
    }

    telemetry = TelemetryModel(**telemetry_params)
    in_memory_storage = TelemetryInMemoryStorage()
    aggr_telem_query_params = in_memory_storage._get_aggr_telem_query_params(telemetry)
    assert isinstance(aggr_telem_query_params, dict)
    keys = [
        "telemetry_type",
        "source_name",
        "category",
        "sub_category",
        "process_type",
        "from_date_time",
        "to_date_time",
    ]
    assert all([key in aggr_telem_query_params.keys() for key in keys])
    assert not [key for key in aggr_telem_query_params.keys() if key not in keys]


def test_in_memory_storage_creates_db_in_memory():
    """Test in memory storage instance has db_in_memory and db_cursor"""
    in_memory_storage = TelemetryInMemoryStorage()
    assert in_memory_storage.db_in_memory
    assert in_memory_storage.db_cursor
    assert isinstance(in_memory_storage.db_in_memory, sqlite3.Connection)
    assert isinstance(in_memory_storage.db_cursor, sqlite3.Cursor)


def test_store_telemetry_raise_exception_when_db_is_closed():
    """Test in memory storage instance has db_in_memory and db_cursor"""
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.close_db()
    with pytest.raises(exceptions.StorageNotInitialized):
        in_memory_storage.store_telemetry(
            TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
        )


def test_select_records_raise_exception_when_db_is_closed():
    """Test in memory storage instance has db_in_memory and db_cursor"""
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.close_db()
    with pytest.raises(exceptions.StorageNotInitialized):
        in_memory_storage.select_records(**telemetry_query_params())


def test_close_db_in_memory():
    """Test in memory storage close method close the db."""
    in_memory_storage = TelemetryInMemoryStorage()
    db_in_memory = in_memory_storage.db_in_memory
    cursor = in_memory_storage.db_cursor
    assert db_in_memory
    assert cursor
    in_memory_storage.close_db()
    with pytest.raises(sqlite3.ProgrammingError):
        cursor.execute("SELECT * FROM telemetry ")
    with pytest.raises(sqlite3.ProgrammingError):
        db_in_memory.cursor()


def test_close_db_in_memory_can_be_closed_twice():
    """
    Test in memory storage close method can be called
    when database is already closed.
    """
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.close_db()
    assert in_memory_storage.close_db() is None


def test_in_memory_strorage_is_only_created_once():
    """Test that once the database is created it will not be reinitialized"""
    in_memory_storage = TelemetryInMemoryStorage()
    db = in_memory_storage.db_in_memory
    TelemetryInMemoryStorage.initialize_db()
    assert in_memory_storage.db_in_memory is db
    new_in_memory_storage = TelemetryInMemoryStorage()
    assert new_in_memory_storage.db_in_memory is db


def test_store_telemetry_stores_object():
    """Test in memory storage instance has db_in_memory and db_cursor"""
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry "
    )
    assert len(all_in_memory_objects.fetchall()) == 1


def test_select_records_returns_sql_lite_cursor():
    """Test select_records method returns sqllite Cursor with one object."""
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    selected_in_memory_objects = in_memory_storage.select_records(
        **telemetry_query_params()
    )
    assert len(selected_in_memory_objects.fetchall()) == 1
    assert isinstance(selected_in_memory_objects, sqlite3.Cursor)


def test_records_with_outside_date_range_are_not_returned():
    """
    Test select_records method returns only those records within the given date
    range.
    """
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(
        TelemetryModel(
            **DEFAULT_TELEMETRY_MODEL_PARAMS
            | {"start_date_time": datetime.now() - timedelta(days=2)}
        )
    )
    selected_in_memory_objects = in_memory_storage.select_records(
        **telemetry_query_params()
    )
    assert len(selected_in_memory_objects.fetchall()) == 1
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry "
    )
    assert len(all_in_memory_objects.fetchall()) == 2


def test_select_records_returns_only_selected_records():
    """
    Test select_records method returns only records accordding to giv.encode()attriubures.
    """
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(
        TelemetryModel(
            **DEFAULT_TELEMETRY_MODEL_PARAMS | {"category": "different_category"}
        )
    )
    selected_in_memory_objects = in_memory_storage.select_records(
        **telemetry_query_params()
    )
    assert len(selected_in_memory_objects.fetchall()) == 2
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry "
    )
    assert len(all_in_memory_objects.fetchall()) == 3


@freeze_time("2022-01-18 18:00:00.123456")
def test_store_telemetry_stores_object_with_create_date(mocker):
    """Test in memory storage instance has db_in_memory and db_cursor"""
    frozen_time = {"start_date_time": datetime.now()}
    telemetry = DEFAULT_TELEMETRY_MODEL_PARAMS | frozen_time
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**telemetry))
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    assert in_memory_record["start_date_time"] == "2022-01-18T18:00:00.123456"


def test_telemetry_storage_to_object_returns_telemetry_model():
    """
    Test _telemetry_storage_to_object method returns a TelemetryModel instance
    created from an in memory storage object.
    """
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    telemetry = in_memory_storage._telemetry_storage_to_object(in_memory_record)
    assert isinstance(telemetry, TelemetryModel)


def test_telemetry_storage_to_object_returns_object_with_correct_values():
    """
    Test _telemetry_storage_to_object method returns a TelemetryModel instance
    with the correct values.
    """
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    telemetry = in_memory_storage._telemetry_storage_to_object(in_memory_record)
    for key, value in DEFAULT_TELEMETRY_MODEL_PARAMS.items():
        assert getattr(telemetry, key) == value


def test_telemetry_storage_to_object_returns_object_with_telemetry_data():
    """
    Test _telemetry_storage_to_object method returns a TelemetryModel instance
    with the correct values.
    """
    counter_key = "TEST_COUNTER"
    telemetry = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    sub_process = telemetry.get_sub_process_data("sub_process")
    sub_process.increase_base_count(increment=1)
    sub_process.increase_custom_count(increment=2, counter=counter_key)
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(telemetry)
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    telemetry_model = in_memory_storage._telemetry_storage_to_object(in_memory_record)
    telemetry_data = telemetry_model.get_sub_process_data("sub_process")
    assert telemetry_data
    assert getattr(telemetry_data, st.BASE_COUNT_KEY) == 1
    assert getattr(telemetry_data, st.COUNTERS_KEY)[counter_key] == 2


@freeze_time("2022-01-18 18:00:00.123456")
def test_get_aggr_telem_date_time_range():
    """
    Test _get_aggr_telem_date_time_range returns the proper date time range.
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "telemetry_type": "DAILY AGGREGATION"
    }
    telemetry = Telemetry(**telemetry_params)
    telemetry._telemetry.start_date_time = datetime.now()
    telemetry.start_date_time
    aggr_telem_date_time_range = (
        TelemetryInMemoryStorage()._get_aggr_telem_date_time_range(telemetry)
    )

    assert isinstance(aggr_telem_date_time_range, DateTimeRange)
    assert aggr_telem_date_time_range.from_date == datetime(2022, 1, 18)
    assert aggr_telem_date_time_range.to_date == datetime(2022, 1, 19)


@freeze_time("2022-01-18 18:00:00.123456")
def test_get_aggr_telem_date_time_range_monthly_aggr():
    """
    Test _get_aggr_telem_date_time_range returns the proper date time range
    with monthly telemetry aggregation type
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "telemetry_type": "MONTHLY AGGREGATION"
    }
    telemetry = Telemetry(**telemetry_params)
    telemetry._telemetry.start_date_time = datetime.now()
    telemetry.start_date_time
    aggr_telem_date_time_range = (
        TelemetryInMemoryStorage()._get_aggr_telem_date_time_range(telemetry)
    )

    assert aggr_telem_date_time_range.from_date == datetime(2022, 1, 1)
    assert aggr_telem_date_time_range.to_date == datetime(2022, 2, 1)


@freeze_time("2022-01-18 18:00:00.123456")
def test_get_aggr_telem_date_time_range_weekly_aggr():
    """
    Test _get_aggr_telem_date_time_range returns the proper date time range
    with weekly telemetry aggregation type
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "telemetry_type": "WEEKLY AGGREGATION"
    }
    telemetry = Telemetry(**telemetry_params)
    telemetry._telemetry.start_date_time = datetime.now()
    telemetry.start_date_time
    aggr_telem_date_time_range = (
        TelemetryInMemoryStorage()._get_aggr_telem_date_time_range(telemetry)
    )

    assert aggr_telem_date_time_range.from_date == datetime(2022, 1, 17)
    assert aggr_telem_date_time_range.to_date == datetime(2022, 1, 24)


def test_delete_telemetry_deletes_telemetry_record():
    """
    Test _telemetry_storage_to_object method returns a TelemetryModel instance
    with the correct values.
    """
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    telemetry = in_memory_storage._telemetry_storage_to_object(in_memory_record)
    for key, value in DEFAULT_TELEMETRY_MODEL_PARAMS.items():
        assert getattr(telemetry, key) == value
