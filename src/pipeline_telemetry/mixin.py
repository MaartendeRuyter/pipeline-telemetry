"""
Module to define TelemetryMixin class for adding methods to
a class that allow easy Telemetry updates
"""

from typing import Any, List, Union

from errors import ReturnValueWithStatus

from .helper import (
    add_errors_from_return_value,
    add_telemetry_counters_from_return_value,
)
from .main import Telemetry
from .settings.data_class import TelemetryCounter


class TelemetryMixin:
    _telemetry: Telemetry

    def process_errors_from_return_value(
        self, sub_process: str, return_value: ReturnValueWithStatus
    ) -> None:
        """
        Adds errors from return_value to _telemetry object for a specific
        sub_process.

        Args:
            sub_process (str):
                One of the sub_processed defined in process type for this
                telemetry object.
            return_value (ReturnValueWithStatus):
                Return value object containing the errors
        """
        add_errors_from_return_value(
            object_with_telemetry=self,
            sub_process=sub_process,
            return_value=return_value,
        )

    def process_telemetry_counters_from_return_value(
        self, return_value: ReturnValueWithStatus
    ) -> List[Any]:
        """
        Adds TelemetryCounters from return_value to _telemetry object for a
        specific sub_process.

        Args:
            return_value (ReturnValueWithStatus):
                Return value object containing the errors

        Returns:
            List:
                List with all value from return_value.result that are not of
                type TelemetryCounter. I.e. all the result entries that are not
                processed by this method.
        """
        return add_telemetry_counters_from_return_value(
            object_with_telemetry=self, return_value=return_value
        )

    def process_telemetry_counters_from_list(
        self, result_list: List[Union[Any, TelemetryCounter]]
    ) -> list[Any]:
        """
        Adds TelemetryCounters from result_list to _telemetry object.

        Args:
            result_list ([Any, TelemetryCounter]):
                Result list containing data objects (not processed) and
                Telemetry counters

        Returns:
            List:
                List with all data objects from result_list. All objects of type
                TelemetryCounter will have been removed.
        """
        return_value = ReturnValueWithStatus(result=result_list)
        return self.process_telemetry_counters_from_return_value(return_value)

    def set_telemetry_source_name(self, source_name: str) -> None:
        """(re)Set the telemerty source name

        Args:
            source_name (str): The source_name that should be added to the
                               telemetry object.
        """
        self._telemetry.telemetry.source_name = source_name
