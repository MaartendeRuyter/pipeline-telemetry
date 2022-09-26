from datetime import datetime
from typing import Iterator, List

from test_data import DEFAULT_TELEMETRY_MODEL_PARAMS

from pipeline_telemetry.data_classes import TelemetryData, TelemetryModel

TELEMETRY_MODEL_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)

telemetry_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
telemetry_data_2 = TelemetryData(base_counter=1)
telemetry_model_2.telemetry.update({'DATA_STORAGE': telemetry_data_2})

telemetry_model_3 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
telemetry_data_3 = TelemetryData(base_counter=2, fail_counter=1)
telemetry_model_3.telemetry.update({'DATA_STORAGE': telemetry_data_3})



class TelemetryTestList():
    __telemetry_models: List[TelemetryModel] = [
        TELEMETRY_MODEL_1, telemetry_data_2, telemetry_model_3]

    def telemetry_list(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database query with the provided arguments.
        """
        for telemetry_model in self.__telemetry_models:
            yield telemetry_model