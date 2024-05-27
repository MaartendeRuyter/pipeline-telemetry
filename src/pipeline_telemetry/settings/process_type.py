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


class ProcessTypesMeta(type):
    _process_types: list[ProcessType] = []

    def __new__(cls, name, bases, class_dict):
        process_types: list[ProcessType] = []

        for mixin_class in bases:
            for process_type_key in dir(mixin_class):
                process_type = getattr(mixin_class, process_type_key)
                if type(process_type) is ProcessType:
                    # ensure that all process types are registered in the ProcesTypes class
                    # also when using the metaclass. Other wise use of a ProcesType defined
                    # via the metaclass will be found invalidat when used in Telemetry Class
                    ProcessTypes.register_process_type(process_type_key, process_type)
                    process_types.append(process_type)

        # Add the ProcesTypes class to the based so that ProcesTypes methods are included
        # in the returned class definition.
        bases_list = list(bases)
        bases_list.append(ProcessTypes)
        bases_with_proces_types = tuple(bases_list)

        class_dict["_process_types"] = process_types
        return type.__new__(cls, name, bases_with_proces_types, class_dict)

    # Empty methods defined in meta class to ensure typing and autocompletion is working
    @classmethod
    def register_process_type(
        cls, process_type_key: str, process_type: ProcessType
    ) -> None:
        """Class method to register a single process type."""
        ...

    @classmethod
    def register_process_types(cls, process_types: type[BaseEnumerator]) -> None:
        """Class method to register new errors from enumerator."""
        ...

    @classmethod
    def is_registered(cls, process_type: ProcessType) -> bool:
        """Method checks of a process_type is registered.

        Args:
            process_type (ProcessType): ProcessType instance to be checked

        Returns:
            Bool: True of process_type is registered else False
        """
        raise NotImplementedError
