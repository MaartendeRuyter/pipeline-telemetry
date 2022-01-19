"""Module to test storage module.
"""
import sqlite3

from freezegun import freeze_time

from pipeline_telemetry.settings.settings import DEFAULT_TRAFIC_LIGHT_COLOR
from pipeline_telemetry.storage.generic import AbstractTelemetryStorage
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage
from pipeline_telemetry.storage.mongo import TelemetryMongoModel, \
    TelemetryMongoStorage
from pipeline_telemetry.storage.mongo_connection import get_mongo_db_port


def test_abstract_strorage_class_exists():
    """Test abstract storage class exists."""
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
    telemetry = {"source_name": "test"}
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(telemetry)
    all_in_memory_objects = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry "
    )
    assert len(all_in_memory_objects.fetchall()) == 1


@freeze_time("2022-01-18 18:00:00.123456")
def test_store_telemetry_stores_object_with_create_date(mocker):
    """Test in memory storage instance has db_in_memory and db_cursor"""
    telemetry = {"source_name": "test"}
    # Table reset for each test is needed as the table is a class property
    TelemetryInMemoryStorage._define_db_table(TelemetryInMemoryStorage.db_cursor)
    in_memory_storage = TelemetryInMemoryStorage()
    in_memory_storage.store_telemetry(telemetry)
    in_memory_record = in_memory_storage.db_cursor.execute(
        "SELECT * FROM telemetry LIMIT 1"
    ).fetchone()
    assert in_memory_record[7] == "2022-01-18 18:00:00.123456"


def test_telemetry_mongo_model_class_exists():
    """Test TelemetryMongoModel class exists."""
    assert TelemetryMongoModel


def test_telemetry_mongo_storage_class_exists():
    """Test TelemetryMongoStorage class exists."""
    assert TelemetryMongoStorage


def test_store_telemetry_method_processes_and_saves_telemetry(mocker):
    """
    Test store_telemetry method calls _telemetry_model_kwargs and then creates
    and saves a mongo object.
    """
    mongo_module_path = "pipeline_telemetry.storage.mongo."
    mocker.patch(mongo_module_path + "TelemetryMongoModel.save", return_value=True)
    mocker.patch(
        mongo_module_path + "TelemetryMongoStorage._telemetry_model_kwargs",
        return_value={},
    )
    _telemetry_model_kwargs_spy = mocker.spy(
        TelemetryMongoStorage, "_telemetry_model_kwargs"
    )
    _telemetry_mongo_model_new_spy = mocker.spy(TelemetryMongoModel, "__new__")
    _telemetry_mongo_model_save_spy = mocker.spy(TelemetryMongoModel, "save")
    TelemetryMongoStorage().store_telemetry(telemetry={"source_name": "test"})
    assert _telemetry_model_kwargs_spy.called
    assert _telemetry_mongo_model_new_spy.called
    assert _telemetry_mongo_model_save_spy.called


def test_telemetry_model_kwargs_method():
    """Test _telemetry_model_kwargs method returns correct kwargs."""
    result = TelemetryMongoStorage()._telemetry_model_kwargs(
        {
            "category": "test",
            "sub_category": "sub_test",
            "source_name": "tst_source_name",
            "process_type": "tst_process_type",
            "start_date_time": "tst_start_date_time",
            "run_time_in_seconds": "tst_run_time_in_seconds",
            "field1": {"a": 1},
            "field2": "value",
            "traffic_light": DEFAULT_TRAFIC_LIGHT_COLOR,
        }
    )

    assert result == {
        "category": "test",
        "sub_category": "sub_test",
        "source_name": "tst_source_name",
        "process_type": "tst_process_type",
        "start_date_time": "tst_start_date_time",
        "run_time_in_seconds": "tst_run_time_in_seconds",
        "telemetry": {"field1": {"a": 1}, "field2": "value"},
        "traffic_light": DEFAULT_TRAFIC_LIGHT_COLOR,
    }


def test_get_mongo_db_port_returns_none():
    """Test _get_mongo_db_port returns None if no env variable is set."""
    assert get_mongo_db_port() is None


def test_get_mongo_db_port_returns_port_int(mocker):
    """Test _get_mongo_db_port returns port nr as intno env variable is set."""
    mocker.patch("os.getenv", return_value="12345")
    assert get_mongo_db_port() == 12345


def test_default_access_params():
    """Test default_access_params are set poperly."""
    from pipeline_telemetry.storage import mongo_connection as mc

    def_params = mc.MONGO_ACCESS_PARAMS
    assert def_params["port"] == mc.DEFAULT_MONGO_DB_PORT
    assert def_params["host"] == mc.DEFAULT_MONGO_DB_HOST
