"""
Module to provide Telemetry class as public class to be accessed

classes
    - CheckForErrors
"""
from datetime import datetime
from typing import List

from errors.base import ErrorCode

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.process_type import ProcessType, ProcessTypes
from pipeline_telemetry.storage import AbstractTelemetryStorage, \
    TelemetryInMemoryStorage
from pipeline_telemetry.validators.dict_validator import DictValidator

# default telemetry field names
BASE_COUNT_KEY = 'base_counter'
FAIL_COUNT = 'fail_counter'
PROCESS_NAME = 'process_name'
PROCESS_TYPE_KEY = 'process_type'
START_TIME = 'start_date_time'
RUN_TIME = 'run_time_in_seconds'


def _raise_exception_if_telemetry_closed(method):
    """
    Decorator method to check if telemetry object is closed.
    If so an exception is raised.

    Decorator method to be used for methods that are only allowed
    when telemtry object not yet closed.
    """

    def wrapper(self, *args, **kwargs):
        """
        Wrapper to check if run_time has been set
        If so the telemetry object is closed
        """
        if self.telemetry.get(RUN_TIME):
            raise exceptions.TelemetryObjectAlreadyClosed()

        return method(self, *args, **kwargs)
    return wrapper


class Telemetry():
    """class to manage the telemetry data object of a data pipeline process


    public class methods:


    """

    _available_process_types = ProcessTypes

    def __init__(
            self, process_name: str, process_type: ProcessType,
            telemetry_rules: dict = None,
            storage_class: AbstractTelemetryStorage = None):
        self._set_process_type(process_type)
        self._telemetry = {
            PROCESS_NAME: process_name,
            PROCESS_TYPE_KEY: self._process_type.name,
            START_TIME: datetime.now()
        }
        self._telemetry_rules = telemetry_rules or {}
        self._storage_class = self._get_storage_class(storage_class)

    @classmethod
    def add_process_type(
            cls, process_type_key: str, process_type: ProcessType) -> None:
        """
        Add a custom process type to the available process types.

        Args:
            process_type (ProcessType): Process type that needs to be added
            process_type_key (str): key that should be used when calling this
                                    ProcessType
        """
        if not isinstance(process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType()
        cls._available_process_types.register_process_type(
            process_type_key, process_type)

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
    def process_name(self) -> str:
        """Process_name property."""
        return self._telemetry.get(PROCESS_NAME)

    @property
    def telemetry(self) -> dict:
        """Telemetry property."""
        return self._telemetry

    @property
    def sub_process_types(self) -> list:
        """Returns a of subprocess types allowed for the Telemetry instance."""
        return self._process_type.sub_processes

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
        if self._telemetry.get(RUN_TIME):
            raise exceptions.TelemetryObjectAlreadyClosed()
        self._telemetry[RUN_TIME] = (datetime.now() -
                                     self._telemetry.get(START_TIME)).total_seconds()

        self._storage_class.store_telemetry(self._telemetry)

        return self._telemetry

    @_raise_exception_if_telemetry_closed
    def add(self, sub_process: str,
            data: dict, errors: List[ErrorCode]) -> None:
        """
        Add data validation errors and/or errors from data process to a
        telemetry sub process.

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
            error_code = error.code
            self.increase_sub_process_custom_count(
                custom_counter=error_code,
                sub_process=sub_process)

    @ _raise_exception_if_telemetry_closed
    def increase_sub_process_base_count(self, sub_process: str) -> None:
        """
        Increases the base count for a subprocess.

        Args:
            sub_process (str): name of subprocess
        """
        if not self._telemetry.get(sub_process):
            self._initialize_sub_process(sub_process)

        self._telemetry[sub_process][BASE_COUNT_KEY] += 1

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_fail_count(self, sub_process: str) -> None:
        """Increases the fail count for a subprocess

        Args:
            sub_process (str): name of subprocess
        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if not self._telemetry.get(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        self._telemetry[sub_process][FAIL_COUNT] += 1

    @_raise_exception_if_telemetry_closed
    def increase_sub_process_custom_count(
            self, custom_counter: str, sub_process: str,
            increment: int = 1) -> None:
        """
        Increases a custom counter for a subprocess.

        Args:
            sub_process (str): name of subprocess
            custom_counter (str): name of custom counter
            increment (int): increment for the counter

        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if not self._telemetry.get(sub_process):
            raise exceptions.BaseCountForSubProcessNotAdded(sub_process)

        if not self._telemetry[sub_process].get(custom_counter):
            self._telemetry[sub_process][custom_counter] = 0

        self._telemetry[sub_process][custom_counter] += increment

    @_raise_exception_if_telemetry_closed
    def increase_custom_count(
            self, custom_counter: str, increment: int = 1) -> None:
        """
        Increases a custom counter for the telemetry object.

        Args:
            custom_counter (str): name of custom counter
            increment (int): increment for the counter

        Raises:
            BaseCountForSubProcessNotAdded: if subprocess has not yet been
                                            created
        """
        if not self._telemetry.get(custom_counter):
            self._telemetry[custom_counter] = 0

        self._telemetry[custom_counter] += increment

    def _initialize_sub_process(self, sub_process: str) -> None:
        """sets the initial count object for a sub_process

        Args:
            sub_process (str): sub process name
        """
        if sub_process not in self._process_type.sub_processes:
            raise exceptions.InvalidSubProcess(sub_process, self._process_type)

        self._telemetry[sub_process] = {
            BASE_COUNT_KEY: 0,
            FAIL_COUNT: 0}

    def _set_process_type(self, process_type: ProcessType) -> None:
        """Sets the process type for the telemetrty instance."""
        if not isinstance(process_type, ProcessType):
            raise exceptions.ProcessTypeMustBeOfClassProcessType
        if not self._available_process_types.is_registered(process_type):
            raise exceptions.ProcessTypeNotRegistered(process_type)
        self._process_type = process_type
