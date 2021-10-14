"""
Module to provide Telemetry class as public class to be accessed

classes
    - CheckForErrors
"""
from datetime import datetime

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.settings import BASE_SUB_PROCESS_TYPES
from pipeline_telemetry.storage import AbstractTelemetryStorage, \
    TelemetryInMemoryStorage

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

    _sub_process_types = BASE_SUB_PROCESS_TYPES

    def __init__(
            self, process_name: str, process_type: str,
            telemetry_rules: dict = dict,
            storage_class: AbstractTelemetryStorage = None):
        self._telemetry = {
            PROCESS_NAME: process_name,
            PROCESS_TYPE_KEY: process_type,
            START_TIME: datetime.now()
        }
        self._telemetry_rules = telemetry_rules
        self._storage_class = self._get_storage_class(storage_class)
        self._validate_initial_telemetry()

    @classmethod
    def add_process_type(cls, process_type: dict) -> None:
        """Add a custom process type and sub process types to the class

        Args:
            process_type (dict):
                dict describing the process and sub_process types
        """
        if not isinstance(process_type, dict):
            raise exceptions.ProcessTypeMustBeDict()
        cls._sub_process_types.update(process_type)

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
        """ process_name property """
        return self._telemetry.get(PROCESS_NAME)

    @property
    def telemetry(self) -> dict:
        """ telemetry property """
        return self._telemetry

    @property
    def process_types(self) -> list:
        """ returns a list of process_types """
        # process types are the keys in sub_process_list
        return list(self._sub_process_types.keys())

    @property
    def sub_process_types(self) -> dict:
        """ returns a dict of process_type including their sub_process type """
        return self._sub_process_types

    def save_and_close(self) -> dict:
        """
        closes and stores the telemetry instance and returns the
        telemetry value

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
    def increase_sub_process_base_count(self, sub_process: str) -> None:
        """Increases the base count for a subprocess

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
        """Increases a custom counter for a subprocess

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
        """Increases a custom counter for the telemetry object

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
        self._telemetry[sub_process] = {
            BASE_COUNT_KEY: 0,
            FAIL_COUNT: 0}

    def _validate_initial_telemetry(self) -> None:
        """ validates telemetry initial settings
        Initial settings are programmatically set and should therefor always be
        valid

        exception is raised if initial settings are invalid.
        """
        process_type = self._telemetry.get(PROCESS_TYPE_KEY)
        if process_type not in self.sub_process_types.keys():
            raise exceptions.InvalidProcessType(process_type)
