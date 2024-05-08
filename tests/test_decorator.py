"""Module to test decorator logic."""

import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry.decorator import (
    add_mongo_single_usage_telemetry,
    add_mongo_telemetry,
    add_single_usage_telemetry,
    add_telemetry,
)
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage
from pipeline_telemetry.storage.mongo import TelemetryMongoStorage


def test_default_decorator():
    """
    Test that default decorator does not effect decorated method result
    but sets the telemetry property.
    """

    class DecoratorTest:
        @add_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return "method result"

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == "method result"
    assert hasattr(class_instance, "_telemetry")


def test_mongo_telemetry_decorator(mocker):
    """
    Test that mongo decorator does not effect decorated method result
    but sets the telemetry property.
    """
    mocker.patch(
        "pipeline_telemetry.decorator.TelemetryMongoStorage", TelemetryInMemoryStorage
    )

    class DecoratorTest:
        @add_mongo_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return "method result"

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == "method result"
    assert hasattr(class_instance, "_telemetry")


def test_mongo_telemetry_decorator_sets_mongo_storage_class(mocker):
    """
    Test that mongo decorator sets the mongo storage class
    """
    mongo_module_path = "pipeline_telemetry.storage.mongo."
    mocker.patch(mongo_module_path + "TelemetryMongoModel.save", return_value=None)

    class DecoratorTest:
        @add_mongo_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return self._telemetry.storage_class

    assert issubclass(DecoratorTest().decorated_method(), TelemetryMongoStorage)


def test_calling_mongo_decorated_method_from_within_decorated_method(mocker):
    """
    Test that when telemetry is active it is not changed by any other telemetry
    decorated method that is being called.
    """
    mongo_module_path = "pipeline_telemetry.storage.mongo."
    mocker.patch(mongo_module_path + "TelemetryMongoModel.save", return_value=None)

    changed_telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "category": "OTHER VALUE",
    }

    class DecoratorTestMongo:
        @add_mongo_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return self.second_decorated_method()

        @add_mongo_telemetry(changed_telemetry_params)
        def second_decorated_method(self):
            return self._telemetry.category

    class_instance = DecoratorTestMongo()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == DEFAULT_TELEMETRY_PARAMS.get("category")
    assert hasattr(class_instance, "_telemetry")


def test_calling_decorated_method_from_within_decorated_method():
    """
    Test that when a telemetry instance created with add_telemetry is
    active it is not changed by any other telemetry decorated method that is
    being called.
    """
    changed_telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "category": "OTHER VALUE",
    }

    class DecoratorTest:
        @add_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return self.second_decorated_method()

        @add_telemetry(changed_telemetry_params)
        def second_decorated_method(self):
            return self._telemetry.category

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == DEFAULT_TELEMETRY_PARAMS.get("category")
    assert hasattr(class_instance, "_telemetry")


def test_single_usage_decorator_raises_params_not_def_exc():
    """
    Test that add_single_usage_telemetry decorator raises an exception when
    no telemetry params are defined in class of class instance.
    """

    class DecoratorTest:
        @add_single_usage_telemetry()
        def decorated_method(self):
            return "method result"

    with pytest.raises(exceptions.ClassTelemetryParamsNotDefined) as excep:
        DecoratorTest().decorated_method()
    assert "Telemetry params not defined" in str(excep)


def test_single_usage_class_telemetry_settings():
    """
    Test that add_single_usage_telemetry decorator can use class defined
    telemetry settings.
    """

    class DecoratorTest:
        TELEMETRY_PARAMS = DEFAULT_TELEMETRY_PARAMS

        @add_single_usage_telemetry()
        def decorated_method(self):
            pass

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    class_instance.decorated_method()
    assert hasattr(class_instance, "_telemetry")


def test_single_usage_telemetry_settings_with_sub_process():
    """
    Test that add_single_usage_telemetry decorator can use class defined
    telemetry settings.
    """
    sub_process = DEFAULT_TELEMETRY_PARAMS["process_type"].sub_processes[0]

    class DecoratorTest:
        TELEMETRY_PARAMS = DEFAULT_TELEMETRY_PARAMS

        @add_single_usage_telemetry(sub_process=sub_process)
        def decorated_method(self):
            return self._telemetry

    class_instance = DecoratorTest()

    telemetry = class_instance.decorated_method()
    assert getattr(telemetry.get(sub_process), st.BASE_COUNT_KEY) == 1


def test_single_usage_telemetry_settings_with_mongho_storage(mocker):
    """
    Test that mongo decorator sets the mongo storage class
    """
    mongo_module_path = "pipeline_telemetry.storage.mongo."
    mocker.patch(mongo_module_path + "TelemetryMongoModel.save", return_value=None)

    class DecoratorTest:
        TELEMETRY_PARAMS = DEFAULT_TELEMETRY_PARAMS

        @add_mongo_single_usage_telemetry()
        def decorated_method(self):
            return self._telemetry.storage_class

    assert issubclass(DecoratorTest().decorated_method(), TelemetryMongoStorage)
