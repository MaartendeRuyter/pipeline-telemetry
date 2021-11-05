"""[summary]
"""
from pipeline_telemetry.main import Telemetry


def add_telemetry(telemetry_params: dict) -> object:
    """
    Decorator method to add a telemetry to the class from which the .
    Class instance to which the method belongs should define a method
    result_log_arguments returing a dict with keys:
        reporting_process: process name
        process_type: instance from enumerator ProcessTypes
        process_class: class name of process
        model_type: instance from enumerator ModelTypes
        search_key_type: search key type of data processed
    """

    def wrapper(method):
        def wrapped_method(self, *args, **kwargs):
            """
            Wrapper for method where result log should be added
            """
            if (not hasattr(self, "_telemetry")) or (not self._telemetry):
                self._telemetry = Telemetry(**telemetry_params)
            result = method(self, *args, **kwargs)
            self._telemetry.save_and_close()
            self._telemetry = None
            return result

        return wrapped_method

    return wrapper
