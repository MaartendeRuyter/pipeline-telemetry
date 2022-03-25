"""
Module to provide Telemetry class as public class to be accessed

classes
    - Telemetry

"""
from collections import defaultdict
from datetime import datetime
from typing import List

from errors import ErrorCode

from .helper import _raise_exception_if_telemetry_closed
from .settings import exceptions
from .settings import settings as st
from .settings.data_class import ProcessType, TelemetryCounter
from .settings.process_type import ProcessTypes
from .storage.generic import AbstractTelemetryStorage
from .storage.memory import TelemetryInMemoryStorage
from .validators.dict_validator import DictValidator


class Telemetry:
    """Class to manage the telemetry data object of a data pipeline process.

    This class can be used to measure and store indicators of a data process.
    When the dataprocess is finished this Telemetry object can be persisted in
    a database provide via a storage class.

    args:
        - source_name (str):
            Process name for which telemetry is made for example: `GET-WEATHER`
            Process names can be choosen freely and should ne unique for a
            single process as they are used to collect all telemetry data for a
            specific process.
        - process_type (ProcessType):
            Process Type for which the telemetry is created. For example
            `CREATE_DATA_FROM_API`. Process type are predefined objects and
            made available via class ProcessTypes. Each process type defines
            a number of sub processes like for example `RETRIEVE_RAW_DATA`. For
            these subprocess specific telemetry data can be stored in the
            telemetry instance
        - telemetry_rules (dict)
            rules how to evaluate the data object for specific sub process
            see DictValidator class for more details on how to define rules
        - storage_class (AbstractTelemetryStorage)
            class to define storage method for Telemetry object

    public class methods:
        - add_process_types: add custom process types

    properties:
        - category
        - sub_category
        - source_name
        - process_type
        - sub_process_types

    public methods:
        - get (as normal get method for dict)
        - save_and_close
        - add
        - increase_sub_process_base_count
        - increase_sub_process_fail_count
        - increase_sub_process_custom_count
        - increase_custom_count
    """

    _available_process_types = ProcessTypes
    _available_telemetry_types = st.TELEMETRY_TYPES

    def __init__(
        self,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: ProcessType,
        telemetry_type: str = st.DEFAULT_TELEMETRY_TYPE,
        telemetry_rules: dict = dict(),
        storage_class: AbstractTelemetryStorage = None,
    ):
        self._set_process_type(process_type)
        self._telemetry = defaultdict(int)
        self._validate_telemetry_type(telemetry_type)
        self._telemetry.update({
            st.TELEMETRY_TYPE_KEY: telemetry_type,
            st.CATEGORY_KEY: category,
            st.SUB_CATEGORY_KEY: sub_category,
            st.SOURCE_NAME_KEY: source_name,
            st.PROCESS_TYPE_KEY: self._process_type.name,
            st.START_TIME: datetime.now(),
            st.IO_TIME_KEY: 0,
            st.TRAFFIC_LIGHT_KEY: st.DEFAULT_TRAFIC_LIGHT_COLOR
        })
        self._telemetry_rules = telemetry_rules
        self._storage_class = self._get_storage_class(storage_class)

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

    def _validate_telemetry_type(self, telemetry_type: str) -> None:
        """Check validaty of provided telemetry type.

        Raises exception if not valid. Returns non if telemetry type is valid.

        Args:
            telemetry_type (str): [description]

        Raises:
            exceptions.InvalidTelemetryType: When telemetry type is not valid.
        """

        if telemetry_type not in self._available_telemetry_types:
            raise exceptions.InvalidTelemetryType(
                self._available_telemetry_types)

    @staticmethod
    def _get_storage_class(storage_class: AbstractTelemetryStorage) -> None:
        """
        validates and sets the storage class. If no storage class provided
        it is defaulted to TelemetryInMemoryStorage

        Args:
            storage_class (AbstractTelemetryStorage):
                Storage class, child class from AbstractTelemetryStorage

        Raises:
            StorageClassOfIncorrectType
        """
        # set default in memory storage if no storage class provided
        if not storage_class:
            storage_class = TelemetryInMemoryStorage

        if not issubclass(storage_class, AbstractTelemetryStorage):
            raise exceptions.StorageClassOfIncorrectType(
                storage_class.__class__.__name__
            )

        return storage_class()

    @property
    def storage_class(self):
        return self._storage_class

    @storage_class.setter
    def storage_class(self, storage_class):
        self._storage_class = self._get_storage_class(storage_class)

    @property
    def source_name(self) -> str:
        """Source_name property."""
        return self._telemetry.get(st.SOURCE_NAME_KEY)

    @property
    def traffic_light(self) -> str:
        """Traffic_light property."""
        return self._telemetry.get(st.TRAFFIC_LIGHT_KEY)

    @property
    def telemetry(self) -> dict:
        """Telemetry property."""
        return self._telemetry

    @property
    def sub_process_types(self) -> list:
        """Returns a of subprocess types allowed for the Telemetry instance."""
        return self._process_type.sub_processes

    def set_orange_traffic_light(self) -> None:
        """Sets traffic light attribute to orange."""
        self._telemetry[st.TRAFFIC_LIGHT_KEY] = st.TRAFIC_LIGHT_COLOR_ORANGE

    def set_red_traffic_light(self) -> None:
        """Sets traffic light attribute to red."""
        self._telemetry[st.TRAFFIC_LIGHT_KEY] = st.TRAFIC_LIGHT_COLOR_RED

    def get(self, field_name: str) -> dict:
        """Retrieve a field from the telemetry object.

        Implements the get method on the Telemetry object as if it is a dict

        Returns:
            dict: [description]
        """
        return self._telemetry.get(field_name)

    def save_and_close(self) -> dict:
        """
        Closes and stores the telemetry instance and returns the
        telemetry value.

        Returns:
            dict: telemetry result
        """
        if self._telemetry.get(st.RUN_TIME):
            raise exceptions.TelemetryObjectAlreadyClosed()
        self._set_runtime()
        self._storage_class.store_telemetry(self._telemetry)

        return self._telemetry

    def _set_runtime(self) -> None:
        """Method to calculate and set the runtime seconds (in str)."""
        run_time = datetime.now() - self._telemetry.get(st.START_TIME)
        self._telemetry[st.RUN_TIME] = str(run_time.total_seconds())

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
        if not self._telemetry.get(sub_process):
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

    def _add_errors(self, sub_process: str, errors: list) -> None:
        """Adds the error to a telemetry sub process.

        :param sub_process: applicable subprocess for the errors
        :typesub_process: str
        :param errors: errors to be processed
        :type errors: list of Errorcodes
        :returns: None
        """
        for error in errors:
            self.increase_sub_process_error_count(error=error, sub_process=sub_process)

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_base_count(
        self, sub_process: str, increment: int = 1
    ) -> None:
        """
        Increases the base count for a subprocess.

        Args:
            sub_process (str): name of subprocess
        """
        if not self._telemetry.get(sub_process):
            self._initialize_sub_process(sub_process)

        self._telemetry[sub_process][st.BASE_COUNT_KEY] += increment

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_fail_count(
            self, sub_process: str, increment: int = 1) -> None:
        """Increases the fail count for a subprocess

        Args:
            sub_process (str): name of subprocess
        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if not self._telemetry.get(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        self._telemetry[sub_process][st.FAIL_COUNT_KEY] += increment

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
        if not self._telemetry.get(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        self._telemetry[sub_process][custom_counter] += increment

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_error_count(
        self, sub_process: str, error: ErrorCode, increment: int = 1
    ) -> None:
        """
        Increases a error counter for a subprocess.

        Args:
            sub_process (str): name of subprocess
            error_code (str): error code from ErrorCode object
            increment (int): increment for the counter

        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if not self._telemetry.get(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        self._telemetry[sub_process][st.ERRORS_KEY][error.code] += increment

    @_raise_exception_if_telemetry_closed
    def increase_io_time(self, io_time: float) -> None:
        """
        Increases the io_time of the telemetry object.

        Args:
            io_time (float): io_time that needs to be added to the total io_time
        """
        self._telemetry[st.IO_TIME_KEY] += io_time

    @_raise_exception_if_telemetry_closed
    def increase_custom_count(self, custom_counter: str, increment: int = 1) -> None:
        """
        Increases a custom counter in the top level of the telemetry object.
        When then custom counter does not yet exist is created.

        Args:
            custom_counter (str): name of custom counter
            increment (int): increment for the counter (Default = 1)
        """
        self._telemetry[custom_counter] += increment

    def add_telemetry_counter(
        self, telemetry_counter: TelemetryCounter, increment: int = None
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
        if telemetry_counter.error:
            self.increase_sub_process_error_count(
                sub_process=sub_process,
                error=telemetry_counter.error,
                increment=increment,
            )
        if not telemetry_counter.error:
            self.increase_sub_process_custom_count(
                sub_process=sub_process,
                custom_counter=counter_name,
                increment=increment,
            )

    def _initialize_sub_process(self, sub_process: str) -> None:
        """sets the initial count object for a sub_process

        Args:
            sub_process (str): sub process name
        """
        if sub_process not in self._process_type.sub_processes:
            raise exceptions.InvalidSubProcess(sub_process, self._process_type)

        self._telemetry[sub_process] = defaultdict(int)
        self._telemetry[sub_process].update({
            st.BASE_COUNT_KEY: 0,
            st.FAIL_COUNT_KEY: 0,
            st.ERRORS_KEY: defaultdict(int)
        })

    def _set_process_type(self, process_type: ProcessType) -> None:
        """Sets the process type for the telemetrty instance."""
        if not isinstance(process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType
        if not self._available_process_types.is_registered(process_type):
            raise exceptions.ProcessTypeNotRegistered(process_type)
        self._process_type = process_type
