====================
Custom process types
====================
Custom process types allow you define in detail what process types and sub
process you to use in your telemetry objects. A process type needs to be defined
using data class ``ProcessType`` and can then be registered via either Singleton
class ``ProcessTypes`` or via class ``Telemetry``::

    from pipeline_telemetry import ProcessType

    new_process_type = ProcessType(
        process_name = 'GET_DAT'
    )

