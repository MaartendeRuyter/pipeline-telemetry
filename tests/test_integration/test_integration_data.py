"""Module to define test data for the integration tests"""

from dataclasses import dataclass

from pipeline_telemetry import Telemetry
from pipeline_telemetry.data_classes import TelemetryData
from pipeline_telemetry.settings import settings as st


@dataclass(frozen=True)
class IntegrationTestData:
    """Immutable dataclass to define integration test data."""

    data: dict
    validation_rules: dict
    expected_result: TelemetryData
    result_field: str

    def validate_telemetry_data(self, telemetry: Telemetry) -> bool:
        test_result = telemetry.get(self.result_field)
        expected_result = self.expected_result

        return test_result == expected_result

        # return \
        #     test_result.base_counter == expected_result.base_counter and \
        #     test_result.fail_counter == expected_result.fail_counter and \
        #     test_result.errors == expected_result.errors and \
        #     test_result.counters == expected_result.counters


BASIC_RETRIEVE_DATA_TEST = IntegrationTestData(
    data={
        "items": [
            {"id": 1, "field1": "test"},
            {"id": 2, "field1": "test"},
            {"id": 3, "field1": "test"},
            {"id": 4, "field1": "test"},
        ]
    },
    validation_rules={
        "RETRIEVE_RAW_DATA": {
            "has_key": {"field_name": "items"},
            "validate_entries": {"field_name": "items", "expected_count": 4},
        }
    },
    result_field="RETRIEVE_RAW_DATA",
    expected_result=TelemetryData(**{"base_counter": 1, "fail_counter": 0}),
)

MISSING_KEY_RETRIEVE_DATA_TEST = IntegrationTestData(
    data={"no items key": []},
    validation_rules={"RETRIEVE_RAW_DATA": {"has_key": {"field_name": "items"}}},
    result_field="RETRIEVE_RAW_DATA",
    expected_result=TelemetryData(
        **{
            "base_counter": 1,
            "fail_counter": 0,
            st.ERRORS_KEY: {"HAS_KEY_ERR_0001@KEY_<items>": 1},
        }
    ),
)


MUST_HAVE_KEY_IN_ITEMS_TEST = IntegrationTestData(
    data={"items": [{"key": 1}, {"no_key": 2}]},
    validation_rules={
        "RETRIEVE_RAW_DATA": {
            "entries_have_key": {"field_name": "items", "must_have_key": "key"}
        }
    },
    result_field="RETRIEVE_RAW_DATA",
    expected_result=TelemetryData(
        **{
            "base_counter": 1,
            "fail_counter": 0,
            st.ERRORS_KEY: {"ENTRIES_HAVE_KEY_ERR_003@KEY_<items__key>": 1},
        }
    ),
)

NO_ITEMS_HAVE_MUST_HAVE_KEY_TEST = IntegrationTestData(
    data={"items": [{"no_key": 1}, {"no_key": 2}]},
    validation_rules={
        "RETRIEVE_RAW_DATA": {
            "entries_have_key": {"field_name": "items", "must_have_key": "key"}
        }
    },
    result_field="RETRIEVE_RAW_DATA",
    expected_result=TelemetryData(
        **{
            "base_counter": 1,
            "fail_counter": 0,
            st.ERRORS_KEY: {"ENTRIES_HAVE_KEY_ERR_003@KEY_<items__key>": 2},
        }
    ),
)


ITEMS_FIELD_HAS_DICT_TEST = IntegrationTestData(
    data={"items": {"key": 1, "no_key": 2}},
    validation_rules={
        "RETRIEVE_RAW_DATA": {
            "entries_have_key": {"field_name": "items", "must_have_key": "key"}
        }
    },
    result_field="RETRIEVE_RAW_DATA",
    expected_result=TelemetryData(
        **{
            "base_counter": 1,
            "fail_counter": 0,
            st.ERRORS_KEY: {"ENTRIES_HAVE_KEY_ERR_002@KEY_<items>": 1},
        }
    ),
)
