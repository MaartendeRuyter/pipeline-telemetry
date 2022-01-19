"""Module to test decorator logic.
"""
from test_data import DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry.decorator import add_mongo_telemetry, add_telemetry
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
    mocker.patch("pipeline_telemetry.decorator.TelemetryMongoStorage",
                 TelemetryInMemoryStorage)

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
    class DecoratorTest:
        @add_mongo_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return self._telemetry.storage_class

    class_instance = DecoratorTest()
    assert class_instance.decorated_method() == TelemetryMongoStorage


def test_calling_decorated_method_from_within_decorated_method(mocker):
    """
    Test that when telemetry is active it is not changed by any other telemetry
    decorated method that is being called.
    """
    changed_telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy() | {
        "category": "OTHER VALUE",
    }

    class DecoratorTest:
        @add_mongo_telemetry(DEFAULT_TELEMETRY_PARAMS)
        def decorated_method(self):
            return self.second_decorated_method()

        @add_mongo_telemetry(changed_telemetry_params)
        def second_decorated_method(self):
            return self._telemetry.get("category")

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == DEFAULT_TELEMETRY_PARAMS.get("category")
    assert hasattr(class_instance, "_telemetry")


def test_calling_mongo_decorated_method_from_within_decorated_method():
    """
    Test that when a telemetry instance created with add_mongo_telemetry is
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
            return self._telemetry.get("category")

    class_instance = DecoratorTest()
    assert not hasattr(class_instance, "_telemetry")
    assert class_instance.decorated_method() == DEFAULT_TELEMETRY_PARAMS.get("category")
    assert hasattr(class_instance, "_telemetry")
