
from pipeline_telemetry.cli import main


def test_main():
    assert main([]) == 0
