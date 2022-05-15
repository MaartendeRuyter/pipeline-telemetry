"""
Module to define TelemetryMixin class for adding methods to
a class that allow easy Telemetry updates
"""
from errors import ReturnValueWithStatus

from .helper import add_errors_from_return_value


class TelemetryMixin():

    def process_errors_from_return_values(
            self,  sub_process: str,
            return_value: ReturnValueWithStatus) -> None:
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
            return_value=return_value)
