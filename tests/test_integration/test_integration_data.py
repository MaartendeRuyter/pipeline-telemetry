from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationTestData():
    """Immutable dataclass to define integration test data."""
    data: dict
    validation_rules: dict
    telemetry_result: dict

    @property
    def result_field(self):
        return self.telemetry_result.get('field')

    @property
    def expected_result(self):
        return self.telemetry_result.get('result')


def validate_result_from_telemetry(
        telemetry: dict, test_data: IntegrationTestData) -> bool:
    """
    Validates if the telemetry data is according to expected results as defined
    in IntegrationTestData object test_data
    """
    result_field = test_data.result_field
    expected_result = test_data.expected_result
    return telemetry.get(result_field) == expected_result


BASIC_RETRIEVE_DATA_TEST = IntegrationTestData(
    data={'items': [
        {'id': 1, 'field1': 'test'},
        {'id': 2, 'field1': 'test'},
        {'id': 3, 'field1': 'test'},
        {'id': 4, 'field1': 'test'}]},
    validation_rules={
        'RETRIEVE_RAW_DATA': {
            'has_key': {'field_name': 'items'},
            'validate_entries': {
                'field_name': 'items',
                'expected_count': 4}}},
    telemetry_result={
        'field': 'RETRIEVE_RAW_DATA',
        'result': {'base_counter': 1, 'fail_counter': 0}})

MISSING_KEY_RETRIEVE_DATA_TEST = IntegrationTestData(
    data={'no items key': []},
    validation_rules={
        'RETRIEVE_RAW_DATA': {
            'has_key': {'field_name': 'items'}}},
    telemetry_result={
        'field': 'RETRIEVE_RAW_DATA',
        'result': {
            'base_counter': 1,
            'fail_counter': 0,
            'HAS_KEY_ERR_0001@KEY_<items>': 1}})