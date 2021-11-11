"""[summary]
"""
from dataclasses import dataclass
from typing import Any, List

from errors import ErrorCode

from pipeline_telemetry.settings import exceptions


@dataclass(frozen=True)
class ProcessType:
    """Immutable dataclass to define a process type and its subtypes."""

    process_type: str
    subtypes: list = list

    @property
    def name(self) -> str:
        """Property method to return process key name."""
        return self.process_type

    @property
    def sub_processes(self) -> List[str]:
        """Property method to return list of sub process types."""
        return self.subtypes


@dataclass(frozen=True)
class TelemetryCounter:
    """Immutable dataclass to define a process type and its subtypes."""

    sub_process: str
    process_types: List[ProcessType] = None
    process_type: ProcessType = None
    counter_name: str = None
    increment: int = 1
    error: ErrorCode = None

    def add_to(self, object_with_telemetry: Any, increment: int = None) -> None:
        """
        Method to add to add self (the TelemetryCounter) to an object telemetry
        instance
        """
        object_with_telemetry._telemetry.add_telemetry_counter(
            telemetry_counter=self, increment=increment
        )

    def validate_sub_process(self) -> None:
        """
        Raises exception if sub_process not define in ProcessType in scope.
        """
        subtypes = []
        for process_type in self.all_process_types:
            subtypes.extend(process_type.subtypes)

        if self.sub_process not in subtypes:
            raise exceptions.InvalidSubProcessForProcessType

    @property
    def all_process_types(self) -> List[ProcessType]:
        """Returns all process_types in scope in a list

        Returns:
            List[ProcessType]: list with process_types
        """
        all_process_types = [self.process_type]
        if self.process_types:
            all_process_types.extend(self.process_types)

        return list(
            filter(lambda process_type: process_type is not None, all_process_types)
        )
