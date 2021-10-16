"""Module to test storage module.
"""
import sqlite3

from pipeline_telemetry.storage import AbstractTelemetryStorage, \
    TelemetryInMemoryStorage


def test_abstract_strorage_class_exists():
    """Test abstract storage class exists."""
    assert AbstractTelemetryStorage


def test_in_memory_strorage_class_exists():
    """Test that in memory storage class exists."""
    assert TelemetryInMemoryStorage


def test_in_memory_strorage_creates_db_in_memory():
    """Test in memory storage instance has db_in_memory and db_cursor """
    in_memory_storage = TelemetryInMemoryStorage()
    assert in_memory_storage.db_in_memory
    assert in_memory_storage.db_cursor
    assert isinstance(in_memory_storage.db_in_memory, sqlite3.Connection)
    assert isinstance(in_memory_storage.db_cursor, sqlite3.Cursor)


def test_store_telemetry_stores_object():
    """Test in memory storage instance has db_in_memory and db_cursor """
    telemetry = {'process_name': 'test'}
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(
        TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(telemetry)
    all_in_memory_objects = \
        in_memory_storage.db_cursor.execute('SELECT * FROM telemetry ')
    assert len(all_in_memory_objects.fetchall()) == 1
