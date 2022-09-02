from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import DefaultDict, Dict, Optional

from ..settings import exceptions
from ..settings import settings as st


@dataclass
class TelemetryData():
    base_counter: int = 0
    fail_counter: int = 0
    errors: DefaultDict[str, int] = field(
        default_factory=lambda: defaultdict(int))
    counters: DefaultDict[str, int] = field(
        default_factory=lambda: defaultdict(int))

    def increase_base_count(self, increment: int) -> None:
        self.base_counter += increment

    def increase_fail_count(self, increment: int) -> None:
        self.fail_counter += increment

    def increase_error_count(self, increment: int, error: str) -> None:
        self.errors[error] += increment

    def increase_custom_count(self, increment: int, counter: str) -> None:
        self.counters[counter] += increment


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
    telemetry: Dict[str, TelemetryData] = field(default_factory=dict)

    def validate(self) -> None:
        self._check_telemetry_type()

    def _check_telemetry_type(self) -> None:
        """Check validaty of provided telemetry type.

        Raises exception if not valid. Returns non if telemetry type is valid.

        Args:
            telemetry_type (str): [description]

        Raises:
            exceptions.InvalidTelemetryType: When telemetry type is not valid.
        """
        if self.telemetry_type not in st.TELEMETRY_TYPES:
            raise exceptions.InvalidTelemetryType(
                st.TELEMETRY_TYPES)

    def set_orange_traffic_light(self) -> None:
        """Sets traffic light attribute to orange."""
        self.traffic_light = st.TRAFIC_LIGHT_COLOR_ORANGE

    def set_red_traffic_light(self) -> None:
        """Sets traffic light attribute to red."""
        self.traffic_light = st.TRAFIC_LIGHT_COLOR_RED

