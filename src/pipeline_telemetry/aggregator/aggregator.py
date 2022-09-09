"""
Module to define a the TelemetryAggregator class.

This class creates makes an aggregation from a queryset of telemetry objects.
The aggregation of is added to a telemetry object that is provide to aggregate method of the class instance.

Usage


>>> # create new telemetry object
>>> telemetry_object = Telemetry(**telemtry_params)
>>> # create aggregator
>>> aggregator = TelemetryAggregator(telemetry_object)
>>> # aggregate a telemetry queryset and return the result
>>> aggregated_telemetry = aggregator.aggregate_from(telemetry_queryset)

"""
from typing import Protocol


class TelemetryProtocol(Protocol):
    """For the purpose of the TelemetryAggregator adddimg all the new telemetry needs to be able to ad"""

    def __add__(self, telemetry: 'TelemetryProtocol') -> 'TelemetryProtocol':
        ...


class TelemetryList(Protocol):
    def __next__(self) -> TelemetryProtocol:
        ...

    def __iter__(self) -> 'TelemetryList':
        ...


class TelemetryAggregator():

    __telemetry: TelemetryProtocol

    def __init__(self, telemetry: TelemetryProtocol) -> None:
        self.__telemetry = telemetry

    def aggregate_from(
            self, telemetry_list: TelemetryList) -> TelemetryProtocol:
        for telemetry in telemetry_list:
            self.__telemetry += telemetry
        return self.__telemetry
