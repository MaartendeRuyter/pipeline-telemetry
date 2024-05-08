from datetime import date, datetime, timedelta
from typing import Iterator, List

from test_data import DEFAULT_TELEMETRY_MODEL_PARAMS, DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry import TelemetrySelector
from pipeline_telemetry.data_classes import TelemetryData, TelemetryModel

TEST_TELEMETRY_SELECTOR = TelemetrySelector(**DEFAULT_TELEMETRY_PARAMS)

TODAY = date.today()
YESTERDAY = date.today() - timedelta(days=1)
DAY_BEFORE_YESTERDAY = date.today() - timedelta(days=2)

TELEMETRY_MODEL_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)

telemetry_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
telemetry_data_2 = TelemetryData(base_counter=1)
telemetry_model_2.telemetry.update({"DATA_STORAGE": telemetry_data_2})

telemetry_model_3 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
telemetry_data_3 = TelemetryData(base_counter=2, fail_counter=1)
telemetry_model_3.telemetry.update({"DATA_STORAGE": telemetry_data_3})


class TelemetryTestList:
    __telemetry_models: List[TelemetryModel] = [
        TELEMETRY_MODEL_1,
        telemetry_model_2,
        telemetry_model_3,
    ]
    stored_telemetry: List[TelemetryModel]

    def telemetry_list(
        self,
        telemetry_type: str,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: str,
        from_date_time: datetime,
        to_date_time: datetime,
    ) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database
        query with the provided arguments.
        """
        for telemetry_model in self.__telemetry_models:
            yield telemetry_model

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        if not hasattr(self, "stored_telemetry"):
            self.stored_telemetry = []
        self.stored_telemetry.append(telemetry)
