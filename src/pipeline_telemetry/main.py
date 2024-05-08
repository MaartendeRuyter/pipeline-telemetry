"""
Module to provide Telemetry class as public class to be accessed

classes
    - Telemetry

"""

from datetime import datetime
from typing import Dict, List, Optional, Type

from errors import ErrorCode

from .data_classes.telemetry_models import TelemetryData, TelemetryModel
from .helper import _raise_exception_if_telemetry_closed
from .settings import exceptions
from .settings import settings as st
from .settings.data_class import ProcessType, TelemetryCounter
from .settings.process_type import ProcessTypes
from .storage.generic import AbstractTelemetryStorage
from .storage.memory import TelemetryInMemoryStorage
from .validators.dict_validator import DictValidator


class Telemetry:
    _telemetry: TelemetryModel
    _telemetry_rules: dict
    _storage_class: Type[AbstractTelemetryStorage]
    _available_process_types: Type[ProcessTypes] = ProcessTypes
    _process_type: ProcessType
    _available_telemetry_types = st.TELEMETRY_TYPES

    def __init__(
        self,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: ProcessType,
        telemetry_type: str = st.DEFAULT_TELEMETRY_TYPE,
        telemetry_rules: Optional[dict] = None,
        storage_class: Type[AbstractTelemetryStorage] = TelemetryInMemoryStorage,
    ):
        self._process_type = process_type
        self._validate_process_type()
        self._storage_class = storage_class
        self._telemetry_rules = telemetry_rules or {}
        self._telemetry = TelemetryModel(
            telemetry_type=telemetry_type,
            category=category,
            sub_category=sub_category,
            source_name=source_name,
            process_type=process_type.name,
        )
        self._telemetry.validate()

    @classmethod
    def add_process_type(cls, process_type_key: str, process_type: ProcessType) -> None:
        """
        Add a custom process type to the available process types to the
        already registered process types.

        Args:
            process_type (ProcessType): Process type that needs to be added
            process_type_key (str): key that should be used when calling this
                                    ProcessType
        """
        if not isinstance(process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType()
        cls._available_process_types.register_process_type(
            process_type_key, process_type
        )

    @property
    def storage_class(self) -> Type[AbstractTelemetryStorage]:
        """Storage_class property."""
        return self._storage_class

    @property
    def category(self) -> str:
        """Category property."""
        return getattr(self._telemetry, st.CATEGORY_KEY)

    @property
    def telemetry_type(self) -> str:
        """Telemetry_type property."""
        return getattr(self._telemetry, st.TELEMETRY_TYPE_KEY)

    @property
    def sub_category(self) -> str:
        """Category property."""
        return getattr(self._telemetry, st.SUB_CATEGORY_KEY)

    @property
    def source_name(self) -> str:
        """Source_name property."""
        return getattr(self.telemetry, st.SOURCE_NAME_KEY)

    @property
    def start_date_time(self) -> datetime:
        """start_date_time property."""
        return getattr(self.telemetry, st.START_TIME)

    @property
    def io_time_in_seconds(self) -> float:
        """io_time property."""
        return getattr(self.telemetry, st.IO_TIME_KEY)

    @property
    def run_time(self) -> float:
        """run_time property."""
        return getattr(self.telemetry, st.RUN_TIME)

    @property
    def traffic_light(self) -> str:
        """Traffic_light property."""
        return getattr(self.telemetry, st.TRAFFIC_LIGHT_KEY)

    @property
    def telemetry(self) -> TelemetryModel:
        """Telemetry property."""
        return self._telemetry

    @property
    def telemetry_data(self) -> Dict[str, TelemetryData]:
        """
        Telemetry_data property return only the telemetry datapoints
        datapoints from the telemetry object.
        """
        return getattr(self.telemetry, st.TELEMETRY_FIELD_KEY)

    @property
    def sub_process_types(self) -> list[str]:
        """Returns a of subprocess types allowed for the Telemetry instance."""
        return self._process_type.sub_processes

    def save_and_close(self) -> TelemetryModel:
        """
        Closes and stores the telemetry instance and returns the
        telemetry value.

        Returns:
            dict: telemetry result
        """
        if self.run_time:
            raise exceptions.TelemetryObjectAlreadyClosed()
        self._set_runtime()
        self._storage_class().store_telemetry(self.telemetry)

        return self.telemetry

    def add_telemetry_counter(
        self, telemetry_counter: TelemetryCounter, increment: Optional[int] = None
    ) -> None:
        """
        Method to process a TelemetryCounter object with predefined counters.

        Args:
            telemetry_counter (TelemetryCounter): [description]
            increment (int, None):
                when not None overules the increment setting from
                TelemetryCounter (which defaults to 1)
        """
        telemetry_counter.validate_sub_process()
        sub_process = telemetry_counter.sub_process
        counter_name = telemetry_counter.counter_name
        increment = increment or telemetry_counter.increment

        if self._sub_process_not_yet_initialized(sub_process):
            self._initialize_sub_process(sub_process)

        if telemetry_counter.error:
            self.increase_sub_process_error_count(
                sub_process=sub_process,
                error_code=telemetry_counter.error,
                increment=increment,
            )

        else:
            self.increase_sub_process_custom_count(
                sub_process=sub_process,
                custom_counter=counter_name,
                increment=increment,
            )

    @_raise_exception_if_telemetry_closed
    def add(self, sub_process: str, data: dict, errors: List[ErrorCode]) -> None:
        """
        Add data validation errors and/or errors from data process to a
        telemetry sub process.
        Data validation errors are retrieved from data validation defined in
        telemetry rules.

        Method does not update BASE_COUNT.

        :param sub_process: applicable subprocess for the errors
        :type sub_process: str
        :param data: data generated by subproces for which telemetry
                     needs to be generated
        :param type: dict
        :param errors: errors from data process to be added
        :type errors: list of Errorcodes
        :returns: None
        """
        if self._sub_process_not_yet_initialized(sub_process):
            self._initialize_sub_process(sub_process)
        validation_errors = self._validate_data(sub_process, data)
        # add data validation errors
        self._add_errors(sub_process, validation_errors)

        # add data process errors
        if errors:
            self._add_errors(sub_process, errors)

    def _validate_data(self, sub_process: str, data: dict) -> List[ErrorCode]:
        """Validates the data provided by a subprocess.

        Data is validated based upon telemetry rules for the subprocces

        :param sub_process: applicable subprocess
        :typesub_process: str
        :param data: data provided by subprocess
        :type data: dict
        :returns: list of Errorcodes
        """
        telemetry_rules = self._telemetry_rules.get(sub_process, {})
        return DictValidator().validate(data, telemetry_rules)

    def _add_errors(self, sub_process: str, errors: list[ErrorCode]) -> None:
        """Adds the error to a telemetry sub process.

        :param sub_process: applicable subprocess for the errors
        :typesub_process: str
        :param errors: errors to be processed
        :type errors: list of Errorcodes
        :returns: None
        """
        for error_code in errors:
            self.increase_sub_process_error_count(
                error_code=error_code, sub_process=sub_process
            )

    @_raise_exception_if_telemetry_closed
    def set_orange_traffic_light(self) -> None:
        """Sets traffic light attribute to orange."""
        self.telemetry.set_orange_traffic_light()

    @_raise_exception_if_telemetry_closed
    def set_red_traffic_light(self) -> None:
        """Sets traffic light attribute to red."""
        self.telemetry.set_red_traffic_light()

    def _set_runtime(self) -> None:
        """Method to calculate and set the runtime seconds (in str)."""
        run_time = datetime.now() - self.start_date_time
        setattr(self.telemetry, st.RUN_TIME, round(run_time.total_seconds(), 2))

    def get(self, sub_process: str) -> TelemetryData:
        """Returns the data object for a sub process.

        Args:
            sub_process (str): name of sub_process name

        Raises:
            exceptions.BaseCountForSubProcessNotAdded:
                when subprocess is not yet initialized

        Returns:
            TelemetryData: the sub_process TelemetryData dataclass object
        """
        if self._sub_process_not_yet_initialized(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        return self.telemetry_data[sub_process]

    @_raise_exception_if_telemetry_closed
    def increase_io_time(self, incremental_io_time: float) -> None:
        """
        Increases the io_time of the telemetry object.

        Args:
            io_time (float): io_time that needs to be added to the total io_time
        """
        current_io_time = getattr(self._telemetry, st.IO_TIME_KEY)
        increased_io_time = current_io_time + incremental_io_time
        setattr(self._telemetry, st.IO_TIME_KEY, increased_io_time)

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_base_count(
        self, sub_process: str, increment: int = 1
    ) -> None:
        """
        Increases the base count for a subprocess.

        Args:
            sub_process (str): name of subprocess
        """
        if self._sub_process_not_yet_initialized(sub_process):
            self._initialize_sub_process(sub_process)

        self.get(sub_process).increase_base_count(increment)

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_fail_count(
        self, sub_process: str, increment: int = 1
    ) -> None:
        """
        Increases the fail count for a subprocess.

        Args:
            sub_process (str): name of subprocess
        """
        if self._sub_process_not_yet_initialized(sub_process):
            self._initialize_sub_process(sub_process)

        self.get(sub_process).increase_fail_count(increment)

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_error_count(
        self, sub_process: str, error_code: ErrorCode, increment: int = 1
    ) -> None:
        """
        Increases a error counter for a subprocess.

        Args:
            sub_process (str): name of subprocess
            error_code (ErrorCode): ErrorCode object
            increment (int): increment for the counter

        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if self._sub_process_not_yet_initialized(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        self.get(sub_process).increase_error_count(
            increment=increment, error_code=error_code
        )

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_custom_count(
        self, custom_counter: str, sub_process: str, increment: int = 1
    ) -> None:
        """
        Increases a custom counter for a subprocess.

        Args:
            sub_process (str): name of subprocess
            custom_counter (str): name of custom counter
            increment (int): increment for the counter (default = 1)

        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if self._sub_process_not_yet_initialized(sub_process):
            self._initialize_sub_process(sub_process)

        self.get(sub_process).increase_custom_count(
            increment=increment, counter=custom_counter
        )

    def _sub_process_is_initialized(self, sub_process: str) -> bool:
        """Returns True if provided sub_process is initialized

        Args:
            sub_process (str): sub_process

        Returns:
            bool: True if sub_process is inialized, False otherwise
        """
        return sub_process in self.telemetry_data

    def _sub_process_not_yet_initialized(self, sub_process: str) -> bool:
        """Returns True if provided sub_process is not yet initialized

        Args:
            sub_process (str): sub_process

        Returns:
            bool: True if sub_process is inialized, False otherwis
        """
        return not self._sub_process_is_initialized(sub_process)

    def _validate_process_type(self) -> None:
        """Validates the process type for the telemetrty instance."""
        if not isinstance(self._process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType
        if not self._available_process_types.is_registered(self._process_type):
            raise exceptions.ProcessTypeNotRegistered(self._process_type)

    def _initialize_sub_process(self, sub_process: str) -> None:
        """Initializes a sun process in the telemetry data.

        Args:
            sub_process (str): sub process name
        """
        if sub_process not in self.sub_process_types:
            raise exceptions.InvalidSubProcess(sub_process, self._process_type)

        if sub_process in self.telemetry_data:
            raise exceptions.SubProcessAlreadyInitialized(sub_process)

        self.telemetry_data.update(**{sub_process: TelemetryData()})
