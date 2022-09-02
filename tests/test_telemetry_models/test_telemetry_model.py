"""
Module to test telemetry model class for pipeline telemetry module.
"""
import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st

# pylint: disable=protected-access


def test_telemetry_model_exists():
    """check that TelemetryModel class exists"""
    assert TelemetryModel

def test_check_telemetry_type_raises_exception_with_inv_type():
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy()
    telemetry_params[st.TELEMETRY_TYPE_KEY] = 'invalid'
    with pytest.raises(exceptions.InvalidTelemetryType):
        TelemetryModel(**telemetry_params)._check_telemetry_type()
