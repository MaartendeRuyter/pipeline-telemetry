"""
Module pipeline_telemetry
Providing Telemetry class and functionality to store pipeline telemetry detals
Main usage:

    >>> from pipeline_telemetry.main import Telemetry
    >>> telemetry = Telemetry(
            source_name, process_type, telemetry_rules, storage_class)
    >>> pipeline_telemetry.add(sub_process_type, data, errors)
    >>> pipeline_telemetry.save_and_close()

In this example a telemetry object is created, the result of a sub_process is
then added with either the data resulting from this sub process or the error
that the sub process returned. In the final step the telementry is saved and
closed

Arguments
    - source_name (str):
        Process name for the pipeline process that this telemetry is reporting
        on. Name is free to choose but make sure it is a unique name for each
        unique process as it will otherwise be difficult to use the telemetry
        for monitoring the status of your pipeline processes
    - process_type (str):
        Is one of predefined set of process_type, for example
        `create_data_from_url` or `upload_data`. It is possible to define
        custom process_types. See section on process types.
    - telemetry_rules (dict):
        dict describing any telemetry rules that need to be processed when data
        is added to the telemetry object. With these rules you can define custom
        conditional counts and errors that can be applied to the provided data.
        See telemetry rules section for more detail
    -
"""
from errors import ListErrors

from .decorator import add_mongo_single_usage_telemetry, add_mongo_telemetry, \
    add_single_usage_telemetry, add_telemetry
from .helper import increase_base_count, increase_fail_count, \
    is_telemetry_counter
from .main import Telemetry
from .settings.data_class import ProcessType, TelemetryCounter
from .settings.process_type import ProcessTypes
from .settings.settings import BaseEnumerator, DefaultProcessTypes
from .settings.telemetry_errors import ValidationErrors

ProcessTypes.register_process_types(DefaultProcessTypes)
ListErrors.register_errors(ValidationErrors)
