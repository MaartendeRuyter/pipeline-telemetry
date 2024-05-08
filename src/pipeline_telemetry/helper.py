"""Helper module for pipeline_telemetry"""

from typing import Any, List, Union

from errors import ReturnValueWithStatus

from .settings import exceptions
from .settings import settings as st
from .settings.data_class import TelemetryCounter


def is_telemetry_counter(counter: Union[TelemetryCounter, Any]) -> bool:
    """Method to check in object is an instance of TelemetryCounter."""
    return issubclass(counter.__class__, TelemetryCounter)


def add_errors_from_return_value(
    object_with_telemetry: Any, sub_process: str, return_value: ReturnValueWithStatus
) -> None:
    """
    Helper method to add the errors from a ReturnValueWithStatus instance to the
    telemetry instance of the object_with_telemetry.
    """
    object_with_telemetry._telemetry.add(
        sub_process=sub_process, data=[], errors=return_value.errors
    )


def add_telemetry_counters_from_return_value(
    object_with_telemetry: Any, return_value: ReturnValueWithStatus
) -> List[Any]:
    """
    Helper method to add the TelemetryCounters from a ReturnValueWithStatus
    instance to the telemetry instance of the object_with_telemetry.
    """
    result_without_telemetry_counters = []
    for item in return_value.result:
        if is_telemetry_counter(item):
            object_with_telemetry._telemetry.add_telemetry_counter(item)
        else:
            result_without_telemetry_counters.append(item)

    return result_without_telemetry_counters


def process_return_value(
    object_with_telemetry: Any, sub_process: str, return_value: ReturnValueWithStatus
) -> List[Any]:
    """Processes a return value object.
    All errors and telemetry counters in return_value errors and result list
    will be processed and added to the telemetry object in
    object_with_telemetry. All the other values in the result list are then
    returned as a list.

    Args:
        object_with_telemetry (Any): _description_
        sub_process (str): _description_
        return_value (ReturnValueWithStatus): _description_

    Returns:
        List[Any]: _description_
    """
    add_errors_from_return_value(object_with_telemetry, sub_process, return_value)

    return add_telemetry_counters_from_return_value(object_with_telemetry, return_value)


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
        if getattr(self.telemetry, st.RUN_TIME):
            raise exceptions.TelemetryObjectAlreadyClosed()

        return method(self, *args, **kwargs)

    return wrapper
