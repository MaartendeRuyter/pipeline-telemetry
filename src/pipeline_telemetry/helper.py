"""Helper module for pipeline_telemetry
"""
from typing import Any, Union

from pipeline_telemetry.settings.data_class import TelemetryCounter


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
