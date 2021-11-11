"""Helper module for pipeline_telemetry
"""
from typing import Any, Union

from pipeline_telemetry.settings.data_class import TelemetryCounter


def is_telemetry_counter(counter: Union[TelemetryCounter, Any]) -> bool:
    """Method to check in object is an instance of TelemetryCounter."""
    return issubclass(counter.__class__, TelemetryCounter)
