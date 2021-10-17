"""Module to define ProcesTypes class."""
from pipeline_telemetry.settings.settings import BaseEnumerator, \
    DefaultProcessTypes, ProcessType


class ProcessTypes():
    """Singleton Class for registering process_types"""

    def __new__(cls):
        return cls

    @classmethod
    def register_process_type(
            cls, process_type_key: str, process_type: ProcessType) -> None:
        """Class method to register a single process type."""
        if not isinstance(process_type, ProcessType):
            raise ValueError(
                'provided process type is not of type ProcessType')
        setattr(cls, process_type_key, process_type)

    @classmethod
    def register_process_types(cls, process_types: BaseEnumerator) -> None:
        """Class method to register new errors from enumerator."""
        if not issubclass(process_types, BaseEnumerator):
            raise ValueError(
                'provide process is not a subclas of BaseEnumerator')
        for process_type_key in process_types.keys():
            process_type = process_types[process_type_key].value
            cls.register_process_type(
                process_type_key=process_type_key, process_type=process_type)


ProcessTypes.register_process_types(DefaultProcessTypes)
