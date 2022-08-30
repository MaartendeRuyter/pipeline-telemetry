"""
"""
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Type

from errors import ErrorCode

from .helper import _raise_exception_if_telemetry_closed
from .settings import exceptions
from .settings import settings as st
from .settings.data_class import ProcessType, TelemetryCounter
from .settings.process_type import ProcessTypes
from .storage.generic import AbstractTelemetryStorage
from .storage.memory import TelemetryInMemoryStorage
from .validators.dict_validator import DictValidator


@dataclass
class TelemetryData():
    base_counter: int = 0
    fail_counter: int = 0
    errors: defaultdict[int] = \
        field(default_factory=lambda: defaultdict(int))
    counters: defaultdict[int] = \
        field(default_factory=lambda: defaultdict(int))


@dataclass
class TelemetryModel():
    telemetry_type: str
    category: str
    sub_category: str
    source_name: str
    process_type: str
    start_date_time: datetime = datetime.now()
    run_time_in_seconds: Optional[float] = None
    io_time_in_seconds: float = 0
    traffic_light: str = st.DEFAULT_TRAFIC_LIGHT_COLOR
    telemetry: Dict[str, TelemetryData] = field(default_factory=TelemetryData)


class Telemetry():
    _telemetry: TelemetryModel
    _telemetry_rules: dict
    _storage_class: Type[AbstractTelemetryStorage] = TelemetryInMemoryStorage
    _available_process_types: ProcessTypes = ProcessTypes
    _process_type: ProcessType
    _available_telemetry_types = st.TELEMETRY_TYPES


    def __init__(
        self,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: ProcessType,
        telemetry_type: str = st.DEFAULT_TELEMETRY_TYPE,
        telemetry_rules: dict = dict(),
        storage_class:
            Type[AbstractTelemetryStorage] = TelemetryInMemoryStorage,
    ):
        self._process_type = ProcessType
        self._telemetry = TelemetryModel(**{
            st.TELEMETRY_TYPE_KEY: telemetry_type,
            st.CATEGORY_KEY: category,
            st.SUB_CATEGORY_KEY: sub_category,
            st.SOURCE_NAME_KEY: source_name,
            st.PROCESS_TYPE_KEY: process_type.name,
            st.TRAFFIC_LIGHT_KEY: st.DEFAULT_TRAFIC_LIGHT_COLOR})
        self._validate_telemetry_object()


    @property
    def source_name(self) -> str:
        """Source_name property."""
        return getattr(self._telemetry, st.SOURCE_NAME_KEY)

    @property
    def traffic_light(self) -> str:
        """Traffic_light property."""
        return getattr(self._telemetry, st.TRAFFIC_LIGHT_KEY)

    @property
    def telemetry(self) -> TelemetryModel:
        """Telemetry property."""
        return self._telemetry

    @property
    def sub_process_types(self) -> list[str]:
        """Returns a of subprocess types allowed for the Telemetry instance."""
        return self._process_type.sub_processes


    def _validate_process_type(self) -> None:
        """Sets the process type for the telemetrty instance."""
        if not isinstance(self._process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType
        if not self._available_process_types.is_registered(self._process_type):
            raise exceptions.ProcessTypeNotRegistered(self._process_type)

    def _validate_telemetry_object(self) -> None:
        """Method to run all validations on the telemetry object."""
        self._validate_process_type()        




