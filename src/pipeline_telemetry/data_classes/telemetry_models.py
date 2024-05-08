"""
Module to provide the TelemetryData classes

Dataclasses defined in Module

- TelemetryData: Data class to hold the actual (error)counters in a
                 TelemetryModel object

- TelemetryModel: Data class to define the Telemetry object category, type,
                  source etc. Holds the reference to the actual counters defined
                  in TelemetryData dataclass.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import DefaultDict, Dict, Optional

from errors import ErrorCode

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st


@dataclass
class TelemetryData:
    """
    Class to define the telemetry (error)counters.

    attributes:
    - base_counter (int): counter for the TelemetryData object.
    - fail_counter (int): fail counter for the TelemetryData object.
    - counters (dict): dict of sub (custom) counters [str: int]
    - errors (dict): dict of error counters [str: int]

    public methods:
    - increase_base_count
    - increase_fail_count
    - increase_custom_count
    - increase_error_count

    counters can be added in which case base, fail, custom and error counters
    will be summed up seperately. Add method will return self with added
    TelemetryData object.
    """

    base_counter: int = 0
    fail_counter: int = 0
    counters: DefaultDict[str, int] = field(default_factory=lambda: defaultdict(int))
    errors: DefaultDict[str, int] = field(default_factory=lambda: defaultdict(int))

    def increase_base_count(self, increment: int) -> None:
        """Increase the base counter with a given increment."""
        self.base_counter += increment

    def increase_fail_count(self, increment: int) -> None:
        """Increase the fail counter with a given increment."""
        self.fail_counter += increment

    def increase_error_count(self, increment: int, error_code: ErrorCode) -> None:
        """Increase an error counter with a given increment."""

        error_code_key = error_code.code
        self._increase_error_count(increment=increment, error_code_key=error_code_key)

    def _increase_error_count(self, increment: int, error_code_key: str) -> None:
        self.errors[error_code_key] += increment

    def increase_custom_count(self, increment: int, counter: str) -> None:
        """Increase a custom counter with a given increment."""
        self.counters[counter] += increment

    def __add__(self, telemetry_data: "TelemetryData") -> "TelemetryData":
        """
        Add telemetry_data object to self by adding up all counters seperately.
        """
        self.increase_base_count(telemetry_data.base_counter)
        self.increase_fail_count(telemetry_data.fail_counter)
        for error_code_key, increment in telemetry_data.errors.items():
            self._increase_error_count(
                increment=increment, error_code_key=error_code_key
            )
        for counter, increment in telemetry_data.counters.items():
            self.increase_custom_count(increment=increment, counter=counter)
        return self


@dataclass
class TelemetryModel:
    telemetry_type: str
    category: str
    sub_category: str
    source_name: str
    process_type: str
    start_date_time: datetime = datetime.now()
    run_time_in_seconds: Optional[float] = None
    io_time_in_seconds: float = 0
    traffic_light: str = st.DEFAULT_TRAFIC_LIGHT_COLOR
    telemetry: Dict[str, TelemetryData] = field(default_factory=dict)

    def validate(self) -> None:
        self._check_telemetry_type()

    def copy(self) -> "TelemetryModel":
        """
        Method to return a copy of the telemetry model. In a telemetry copy
        only the attributes telemetry_type, categroy, sub_category, source_name
        and process_type are copied.
        """
        return TelemetryModel(
            telemetry_type=self.telemetry_type,
            category=self.category,
            sub_category=self.sub_category,
            source_name=self.source_name,
            process_type=self.process_type,
        )

    def _check_telemetry_type(self) -> None:
        """Check validaty of provided telemetry type.

        Raises exception if not valid. Returns non if telemetry type is valid.

        Args:
            telemetry_type (str): [description]

        Raises:
            exceptions.InvalidTelemetryType: When telemetry type is not valid.
        """
        if self.telemetry_type not in st.TELEMETRY_TYPES:
            raise exceptions.InvalidTelemetryType(st.TELEMETRY_TYPES)

    def set_orange_traffic_light(self) -> None:
        """Sets traffic light attribute to orange."""
        self.traffic_light = st.TRAFIC_LIGHT_COLOR_ORANGE

    def set_red_traffic_light(self) -> None:
        """Sets traffic light attribute to red."""
        self.traffic_light = st.TRAFIC_LIGHT_COLOR_RED

    def __add__(self, telemetry_model_to_add: "TelemetryModel") -> "TelemetryModel":
        """
        Method to add to telementry model instances.
        Adding a 2 telemetry model instances implies adding all telemetry data
        objects and adding iotime, run time and traffic light attributes to a
        specific counter.
        """
        self.__add_base_count()
        self.__add_sub_process(telemetry_model_to_add=telemetry_model_to_add)
        self.__add_traffic_light(telemetry_model_to_add=telemetry_model_to_add)
        self.__add_io_time(telemetry_model_to_add=telemetry_model_to_add)
        self.__add_run_time(telemetry_model_to_add=telemetry_model_to_add)
        return self

    def __add_base_count(self) -> None:
        """
        Sub method for the __add__ method to increase base_counter of the
        aggregation sub_process when adding TelemetryModel instances.
        """
        self.get_sub_process_data(sub_process=st.AGGREGATION_KEY).increase_base_count(
            increment=1
        )

    def __add_traffic_light(self, telemetry_model_to_add: "TelemetryModel") -> None:
        """
        Sub method for the __add__ method to add the traffic_light value of the
        TelemetryModel instance to be added to the aggregation sub_process.
        """
        self.get_sub_process_data(sub_process=st.AGGREGATION_KEY).increase_custom_count(
            increment=1, counter=telemetry_model_to_add.traffic_light
        )

    def __add_sub_process(self, telemetry_model_to_add: "TelemetryModel") -> None:
        """
        Sub method for the __add__ method to add the sub_processes of the two
        TelemetryModel instances.
        """
        for sub_process in telemetry_model_to_add.telemetry:
            sub_pr = self.get_sub_process_data(sub_process)
            sub_pr += telemetry_model_to_add.get_sub_process_data(
                sub_process=sub_process
            )

    def __add_io_time(self, telemetry_model_to_add: "TelemetryModel") -> None:
        """
        Sub method for the __add__ method to add the rounded io_time of the
        TelemetryModel instance to be added to the aggregation sub_process.
        """
        self.get_sub_process_data(sub_process=st.AGGREGATION_KEY).increase_custom_count(
            increment=round(telemetry_model_to_add.io_time_in_seconds),
            counter=st.IO_TIME_KEY,
        )

    def __add_run_time(self, telemetry_model_to_add: "TelemetryModel") -> None:
        """
        Sub method for the __add__ method to add the rounded run_time of the
        TelemetryModel instance to be added to the aggregation sub_process.
        """
        run_time_in_seconds = telemetry_model_to_add.run_time_in_seconds or 0
        self.get_sub_process_data(sub_process=st.AGGREGATION_KEY).increase_custom_count(
            increment=round(run_time_in_seconds), counter=st.RUN_TIME
        )

    def get_sub_process_data(self, sub_process: str) -> TelemetryData:
        if not self.telemetry.get(sub_process):
            self.telemetry[sub_process] = TelemetryData()
        return self.telemetry[sub_process]
