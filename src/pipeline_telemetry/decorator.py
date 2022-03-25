"""Telemety Decorators to be used whith class methods that need telemetry

decorators:
    - add_telemetry
    - add_mongo_telemetry
    - add_single_usage_telemetry
"""
from functools import wraps

from .main import Telemetry
from .settings import exceptions
from .storage import AbstractTelemetryStorage, TelemetryMongoStorage


def add_telemetry(telemetry_params: dict) -> object:
    """
    Decorator method to add a telemetry to the class from which the
    decorator was called. When using this decorator the storage
    class can be set as wanted but defaults to TelemetryInMemoryStorage.

    Args:
        telemetry_params (dict:
            - source_name (str): free format process name
            - process_type (ProcessType): process type definition
            - telemetry_rules (dict): telemetry rules definition dict
            - storage_class (AbstractTelemetryStorage, optional):
                Storage class to be used to store telemetry instances. Defaults
                to TelemetryInMemoryStorage which stores only in memory.
    """

    def wrapper(method):
        @wraps(method)
        def wrapped_method(self, *args, **kwargs):
            """
            Wrapper for method where result log should be added
            """
            if (not hasattr(self, "_telemetry")) or (not self._telemetry):
                self._telemetry = Telemetry(**telemetry_params)
                result = method(self, *args, **kwargs)
                self._telemetry.save_and_close()
                self._telemetry = None
            else:
                result = method(self, *args, **kwargs)

            return result

        return wrapped_method

    return wrapper


def add_mongo_telemetry(telemetry_params: dict) -> object:
    """
    Decorator method to add a telemetry to the class from which the
    decorator was called. When using this decorator the mongo storage
    class will used.

    Args:
        telemetry_params (dict:
            - source_name (str): free format process name
            - process_type (ProcessType): process type definition
            - telemetry_rules (dict): telemetry rules definition dict
    """

    def wrapper(method):
        @wraps(method)
        def wrapped_method(self, *args, **kwargs):
            """
            Wrapper for method where result log should be added
            """
            if (not hasattr(self, "_telemetry")) or (not self._telemetry):
                self._telemetry = Telemetry(**telemetry_params)
                self._telemetry.storage_class = TelemetryMongoStorage
                result = method(self, *args, **kwargs)
                self._telemetry.save_and_close()
                self._telemetry = None
            else:
                result = method(self, *args, **kwargs)
            return result

        return wrapped_method

    return wrapper


def add_mongo_single_usage_telemetry(sub_process: str = None) -> object:
    """
    Decorator method to add a telemetry to the class from which the
    decorator was called. The telemetry object will be reset each the method
    initiating the telemetry object will be called. This method should be used
    for stand alone telemetry measurements like for example external API calls.
    It can be used to easily store a single event telemetry object.

    This method will persist the telemetry object in MongoDB

    Args:
        - sub_process (str, Optional):
            one of the sub_processes defined with the process_type. A
            counter with value 1 will be created for this sub_process.
            This field is optional, if not provided no counter will be
            added to the telemetry object
    """
    return add_single_usage_telemetry(
        sub_process=sub_process,
        storage_class=TelemetryMongoStorage
    )


def add_single_usage_telemetry(
        sub_process: str = None,
        storage_class: AbstractTelemetryStorage = None) -> object:
    """
    Decorator method to add a telemetry to the class from which the
    decorator was called. The telemetry object will be reset each the method
    initiating the telemetry object will be called. This method should be used
    for stand alone telemetry measurements like for example external API calls.
    It can be used to easily store a single event telemetry object.

    Args:
        - sub_process (str):
            one of the sub_processes defined with the process_type. A
            counter with value 1 will be created for this sub_process.
            This field is optional, if not provided no counter will be
            added to the telemetry object
        - storage_class (AbstractTelemetryStorage):
            Storage class to be used for persisting telemetry objects
    """

    def wrapper(method):
        @wraps(method)
        def wrapped_method(self, *args, **kwargs):
            """
            Wrapper for method where result log should be added
            """
            telemetry_params = getattr(self, 'TELEMETRY_PARAMS', False)
            if not telemetry_params:
                raise exceptions.ClassTelemetryParamsNotDefined(self)

            self._telemetry = Telemetry(**telemetry_params)

            if storage_class:
                self._telemetry.storage_class = storage_class

            # only if sub_process was defined set the base count for that
            # subprocess
            if sub_process:
                self._telemetry.increase_sub_process_base_count(
                    sub_process=sub_process)
            result = method(self, *args, **kwargs)
            self._telemetry.save_and_close()
            self._telemetry = None

            return result

        return wrapped_method

    return wrapper
