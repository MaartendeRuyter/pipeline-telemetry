"""[summary]
"""
from dataclasses import dataclass
from typing import List

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

    process_type: ProcessType
    sub_process: str
    counter_name: str = None
    increment: int = 1
    error: ErrorCode = None

    def validate_sub_process(self) -> None:
        """
        Raises exception if sub_process not define in ProcessType in scope.
        """
        if self.sub_process not in self.process_type.subtypes:
            raise exceptions.InvalidSubProcessForProcessType
