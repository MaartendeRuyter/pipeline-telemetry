"""Module to test storage module.
"""
import sqlite3
from datetime import datetime, timedelta

from freezegun import freeze_time
from test_data import DEFAULT_TELEMETRY_MODEL_PARAMS

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.storage.generic import AbstractTelemetryStorage
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage


def telemetry_query_params():
    """Returns a default set of query params"""
    return  DEFAULT_TELEMETRY_MODEL_PARAMS | {
        'from_date_time': datetime.now() - timedelta(days=1),
        'to_date_time': datetime.now() + timedelta(days=1)
    }


def test_in_abstract_strorage_class_exists():
    """Test that abstract storage class exists."""
    assert AbstractTelemetryStorage


def test_in_memory_strorage_class_exists():
    """Test that in memory storage class exists."""
    assert TelemetryInMemoryStorage


def test_in_memory_strorage_creates_db_in_memory():
    """Test in memory storage instance has db_in_memory and db_cursor"""
    in_memory_storage = TelemetryInMemoryStorage()
    assert in_memory_storage.db_in_memory
    assert in_memory_storage.db_cursor
    assert isinstance(in_memory_storage.db_in_memory, sqlite3.Connection)
    assert isinstance(in_memory_storage.db_cursor, sqlite3.Cursor)


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
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry "
    )
    assert len(all_in_memory_objects.fetchall()) == 1


def test_select_records_returns_sql_lite_cursor():
    """Test select_records method returns sqllite Cursor with one object."""
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    selected_in_memory_objects = \
        in_memory_storage.select_records(**telemetry_query_params())
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
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS | {
            'start_date_time': datetime.now() - timedelta(days=2)}))
    selected_in_memory_objects = \
        in_memory_storage.select_records(**telemetry_query_params())
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
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS))
    in_memory_storage.store_telemetry(
        TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS |
                       {'category': 'different_category'}))
    selected_in_memory_objects = in_memory_storage.select_records(
        **telemetry_query_params())
    assert len(selected_in_memory_objects.fetchall()) == 2
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry ")
    assert len(all_in_memory_objects.fetchall()) == 3


@freeze_time("2022-01-18 18:00:00.123456")
def test_store_telemetry_stores_object_with_create_date(mocker):
    """Test in memory storage instance has db_in_memory and db_cursor"""
    frozen_time = {"start_date_time": datetime.now()}
    telemetry = DEFAULT_TELEMETRY_MODEL_PARAMS | frozen_time
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(
        TelemetryModel(**telemetry))
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    assert in_memory_record[5] == "2022-01-18 18:00:00.123456"
