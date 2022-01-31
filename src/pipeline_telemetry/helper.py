"""Helper module for pipeline_telemetry
"""
from typing import Any, Union

from .settings import exceptions
from .settings import settings as st
from .settings.data_class import TelemetryCounter


def is_telemetry_counter(counter: Union[TelemetryCounter, Any]) -> bool:
    """Method to check in object is an instance of TelemetryCounter."""
    return issubclass(counter.__class__, TelemetryCounter)


def increase_base_count(
    object_with_telemetry: Any, sub_process: str, increment: int = 1
) -> None:
    """
    Helper method to increase base count for a sub_process
    """
    object_with_telemetry._telemetry.increase_sub_process_base_count(
        sub_process=sub_process, increment=increment
    )


def increase_fail_count(
    object_with_telemetry: Any, sub_process: str, increment: int = 1
) -> None:
    """
    Helper method to increase base count for a sub_process
    """
    object_with_telemetry._telemetry.increase_sub_process_fail_count(
        sub_process=sub_process, increment=increment
    )


# decorator method to check status telemetry object
def _raise_exception_if_telemetry_closed(method):
    """
    Decorator method to check if telemetry object is closed.
    If so an exception is raised.

    Decorator method to be used for methods that are only allowed
    when telemetry object not yet closed.
    """

    def wrapper(self, *args, **kwargs):
        """
        Wrapper to check if run_time has been set
        If so the telemetry object is closed
        """
        if self.telemetry.get(st.RUN_TIME):
            raise exceptions.TelemetryObjectAlreadyClosed()

        return method(self, *args, **kwargs)

    return wrapper
