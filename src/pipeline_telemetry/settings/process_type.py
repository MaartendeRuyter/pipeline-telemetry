"""Module to define ProcesTypes class."""

from typing import List, Type

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.data_class import ProcessType
from pipeline_telemetry.settings.settings import BaseEnumerator


class ProcessTypes:
    """Singleton Class for registering process_types"""

    _process_types: List[ProcessType] = []

    def __new__(cls):
        return cls

    @classmethod
    def register_process_type(
        cls, process_type_key: str, process_type: ProcessType
    ) -> None:
        """Class method to register a single process type."""
        if not isinstance(process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType
        setattr(cls, process_type_key, process_type)
        cls._process_types.append(process_type)

    @classmethod
    def register_process_types(cls, process_types: Type[BaseEnumerator]) -> None:
        """Class method to register new errors from enumerator."""
        try:
            if not issubclass(process_types, BaseEnumerator):
                raise exceptions.ProcessTypesMustBeOfClassBaseEnumertor
        except TypeError:
            raise exceptions.ProcessTypesMustBeOfClassBaseEnumertor

        for process_type_key in process_types.keys():
            process_type = getattr(process_types, process_type_key).value
            cls.register_process_type(
                process_type_key=process_type_key, process_type=process_type
            )

    @classmethod
    def is_registered(cls, process_type: ProcessType) -> bool:
        """Method checks of a process_type is registered.

        Args:
            process_type (ProcessType): ProcessType instance to be checked

        Returns:
            Bool: True of process_type is registered else False
        """
        return process_type in cls._process_types
