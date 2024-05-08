"""Module to test settings module."""

from pipeline_telemetry.settings import settings


def test_telemetry_type_settings():
    """
    Test that telemetry type settings is a dict where keys and values are
    in uppercase and where underscores in the keys are replaced by spaces
    in the values.
    """
    for k, v in settings.telemetry_types.items():
        assert k == k.upper()
        assert v == v.upper()
        assert v == k.replace("_", " ")
