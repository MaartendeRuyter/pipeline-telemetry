"""Telemety Decorators to be used whith class methods that need telemetry

decorators:
    - add_telemetry
    - add_mongo_telemetry
"""
from pipeline_telemetry.main import Telemetry, mongo_telemetry


def add_telemetry(telemetry_params: dict) -> object:
    """
    Decorator method to add a telemetry to the class from which the
    decorator was called. When using this decorator the mongo storage
    class will used.

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
        def wrapped_method(self, *args, **kwargs):
            """
            Wrapper for method where result log should be added
            """
            if (not hasattr(self, "_telemetry")) or (not self._telemetry):
                self._telemetry = mongo_telemetry(**telemetry_params)
                result = method(self, *args, **kwargs)
                self._telemetry.save_and_close()
                self._telemetry = None
            else:
                result = method(self, *args, **kwargs)
            return result

        return wrapped_method

    return wrapper
