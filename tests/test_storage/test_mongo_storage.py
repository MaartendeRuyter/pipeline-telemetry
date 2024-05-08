"""Module to test storage module."""

from datetime import datetime, timedelta

from test_data import DEFAULT_TELEMETRY_MODEL_PARAMS

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings.settings import DEFAULT_TRAFIC_LIGHT_COLOR, RUN_TIME
from pipeline_telemetry.storage.mongo import TelemetryMongoModel, TelemetryMongoStorage
from pipeline_telemetry.storage.mongo_connection import get_mongo_db_port


def telemetry_query_params():
    """Returns a default set of query params"""
    return DEFAULT_TELEMETRY_MODEL_PARAMS | {
        "from_date_time": datetime.now() - timedelta(days=1),
        "to_date_time": datetime.now() + timedelta(days=1),
    }


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
        TelemetryModel(
            **{
                "telemetry_type": "test telemetry type",
                "category": "test",
                "sub_category": "sub_test",
                "source_name": "tst_source_name",
                "process_type": "tst_process_type",
                "start_date_time": "tst_start_date_time",
                "run_time_in_seconds": 1.123,
                "io_time_in_seconds": 1.1,
                "traffic_light": DEFAULT_TRAFIC_LIGHT_COLOR,
            }
        )
    )

    assert result == {
        "telemetry_type": "test telemetry type",
        "category": "test",
        "sub_category": "sub_test",
        "source_name": "tst_source_name",
        "process_type": "tst_process_type",
        "start_date_time": "tst_start_date_time",
        "run_time_in_seconds": "1.12",
        "io_time_in_seconds": 1.1,
        "telemetry": {},
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


def test_mongo_model_to_dict():
    """
    Test to_dict method returns a dict with run_time_in_seconds atrribute converted to float.
    """
    telemetry = TelemetryMongoModel()
    telemetry._id = "test _id"
    telemetry.run_time_in_seconds = "1"
    telemetry_to_dict = telemetry.to_dict()
    assert isinstance(telemetry_to_dict, dict)
    assert isinstance(getattr(telemetry, RUN_TIME), str)
    assert isinstance(telemetry_to_dict[RUN_TIME], float)
