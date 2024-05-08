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

from abc import ABC

from pipeline_telemetry.storage import TelemetryMongoStorage

from .aggregator import AbstractAggregator, DailyAggregator, PartialToSingleAggregator
from .helper import TelemetrySelector


class AbstractMongoAggregator(ABC):
    """Class to return a DailyAggregator class with TelemetryMongoStorage.

    When using this aggregator class the storage_class is automatically set
    to TelemetryMongoStorage and can not be provided as argument.

    >>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
    >>> aggeregator = DailyMongoAggregator(
            telemetry_selector=telemetry_selector
        )
    """

    AGGREGATOR_CLASS: type[AbstractAggregator]

    def __new__(cls, telemetry_selector: TelemetrySelector):
        return cls.AGGREGATOR_CLASS(
            telemetry_selector=telemetry_selector,
            telemetry_storage=TelemetryMongoStorage(),
        )


class DailyMongoAggregator(AbstractMongoAggregator):
    """Class to return a DailyAggregator class with TelemetryMongoStorage.

    When using this aggregator class the storage_class is automatically set
    to TelemetryMongoStorage and can not be provided as argument.

    >>> telemetry_selector = TelemetrySelector(
        category, sub_category, source_name, process_type)
    >>> aggeregator = DailyMongoAggregator(
            telemetry_selector=telemetry_selector
        )
    """

    AGGREGATOR_CLASS = DailyAggregator


class PartialToSingleMongoAggregator(AbstractMongoAggregator):
    """
    Class to return a PartialToSingleAggregator class with
    TelemetryMongoStorage.

    When using this aggregator class the storage_class is automatically set
    to TelemetryMongoStorage and can not be provided as argument.
    """

    AGGREGATOR_CLASS = PartialToSingleAggregator
