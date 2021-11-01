"""
Module pipeline_telemetry
Providing Telemetry class and functionality to store pipeline telemetry detals
Main usage:

    >>> from pipeline_telemetry.main import Telemetry
    >>> telemetry = Telemetry(
            process_name, process_type, telemetry_rules, storage_class)
    >>> pipeline_telemetry.add(sub_process_type, data, errors)
    >>> pipeline_telemetry.save_and_close()

In this example a telemetry object is created, the result of a sub_process is
then added with either the data resulting from this sub process or the error
that the sub process returned. In the final step the telementry is saved and
closed

Arguments
    - process_name (str):
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
from .main import Telemetry, mongo_telemetry  # noqa: F401
from .settings import errors  # noqa: F401
from .settings import process_type  # noqa: F401
from .settings.process_type import ProcessTypes  # noqa: F401
from .validators import has_key, validate_entries  # noqa: F401
