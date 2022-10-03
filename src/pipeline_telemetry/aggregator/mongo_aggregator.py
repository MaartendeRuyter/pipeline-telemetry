"""
Module to provide Aggregator classes with predefined TelemetryMongoStorage
as storage class.

All these classes only require a TelemetrySelector upon instantiation and
return the appropriate Aggregator class with TelemetryMongoStorage as storage
class.

>>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
>>> aggeregator = MongoAggregatorClassName(
            telemetry_selector=telemetry_selector
        )

available classes:
- DailyMongoAggregator

"""
from pipeline_telemetry.storage import TelemetryMongoStorage

from .aggregator import DailyAggregator
from .helper import TelemetrySelector


class DailyMongoAggregator():
    """Class to return a DailyAggregator class with TelemetryMongoStorage.

    When using this aggregator class the storage_class is automatically set
    to TelemetryMongoStorage and can not be provided as argument.

    >>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
    >>> aggeregator = DailyMongoAggregator(
            telemetry_selector=telemetry_selector
        )
    """

    def __new__(cls, telemetry_selector: TelemetrySelector):
        return DailyAggregator(
            telemetry_selector=telemetry_selector,
            telemetry_storage=TelemetryMongoStorage()
        )
