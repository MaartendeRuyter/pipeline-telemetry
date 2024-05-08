"""[summary]"""

from enum import Enum
from typing import Callable, Dict, List

import pipeline_telemetry.settings.date_ranges as dr
from pipeline_telemetry.settings.data_class import ProcessType

SINGLE_TELEMETRY_TYPE = "SINGLE TELEMETRY"
DAILY_AGGR_TELEMETRY_TYPE = "DAILY AGGREGATION"
WEEKLY_AGGR_TELEMETRY_TYPE = "WEEKLY AGGREGATION"
MONTHLY_AGGR_TELEMETRY_TYPE = "MONTHLY AGGREGATION"
QUARTERLY_AGGR_TELEMETRY_TYPE = "QUARTERLY AGGREGATION"
PARTIAL_AGGR_TELEMETRY_TYPE = "PARTIAL AGGREGATION"

# Constant to define date_range method specific to a given
# TELEMETRY aggregation type
AGGR_DATE_TIME_RANGE_METHODS: dict[str, Callable] = {
    DAILY_AGGR_TELEMETRY_TYPE: dr.get_daily_date_range_for_single_date,
    WEEKLY_AGGR_TELEMETRY_TYPE: dr.get_weekly_date_range_for_single_date,
    MONTHLY_AGGR_TELEMETRY_TYPE: dr.get_monthly_date_range_for_single_date,
}

DEFAULT_TELEMETRY_TYPE = SINGLE_TELEMETRY_TYPE
TELEMETRY_TYPES: List[str] = [
    PARTIAL_AGGR_TELEMETRY_TYPE,
    DEFAULT_TELEMETRY_TYPE,
    DAILY_AGGR_TELEMETRY_TYPE,
    WEEKLY_AGGR_TELEMETRY_TYPE,
    MONTHLY_AGGR_TELEMETRY_TYPE,
    QUARTERLY_AGGR_TELEMETRY_TYPE,
]

telemetry_types: Dict[str, str] = {
    type.upper().replace(" ", "_"): type.upper() for type in TELEMETRY_TYPES
}

TRAFIC_LIGHT_COLOR_GREEN = "GREEN"
TRAFIC_LIGHT_COLOR_ORANGE = "ORANGE"
TRAFIC_LIGHT_COLOR_RED = "RED"
DEFAULT_TRAFIC_LIGHT_COLOR: str = TRAFIC_LIGHT_COLOR_GREEN


BASE_COUNT_KEY = "base_counter"
ERRORS_KEY = "errors"
COUNTERS_KEY = "counters"
FAIL_COUNT_KEY = "fail_counter"
SOURCE_NAME_KEY = "source_name"
CATEGORY_KEY = "category"
SUB_CATEGORY_KEY = "sub_category"
PROCESS_TYPE_KEY = "process_type"
START_TIME = "start_date_time"
RUN_TIME = "run_time_in_seconds"
TRAFFIC_LIGHT_KEY = "traffic_light"
TELEMETRY_TYPE_KEY = "telemetry_type"
IO_TIME_KEY = "io_time_in_seconds"
TELEMETRY_FIELD_KEY = "telemetry"
AGGREGATION_KEY = "telemetry_aggregation_stats"

DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES = [
    "RETRIEVE_RAW_DATA",
    "DATA_CONVERSION",
    "DATA_STORAGE",
]

DEFAULT_UPLOAD_DATA_SUB_PROCESS_TYPES = [
    "DATA_SELECTION",
    "DATA_CONVERSION",
    "DATA_UPLOAD",
]


class BaseEnumerator(Enum):
    """
    Class to define base enumerator with a keys method.
    Only to be used for defining new enumerators.
    """

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())


class DefaultProcessTypes(BaseEnumerator):
    """
    Class to define the defailt process types with their subtypes
    """

    CREATE_DATA_FROM_URL = ProcessType(
        process_type="create_data_from_url",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    CREATE_DATA_FROM_API = ProcessType(
        process_type="create_data_from_api",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    CREATE_DATA_FROM_FILE = ProcessType(
        process_type="create_data_from_file",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    UPLOAD_DATA = ProcessType(
        process_type="upload_data", subtypes=DEFAULT_UPLOAD_DATA_SUB_PROCESS_TYPES
    )
