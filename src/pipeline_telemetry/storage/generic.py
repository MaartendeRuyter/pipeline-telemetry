"""Module to define abstract storage class
"""
from abc import ABCMeta, abstractmethod


class AbstractTelemetryStorage(metaclass=ABCMeta):
    """ Abstract Telemetry Storage class

    implements store_telemetry method that persists a given telemetry object

    Any class that stores the telemetry objects should be subclassed from
    this Abstract Class
    """
    # pylint: disable=too-few-public-methods

    @abstractmethod
    def store_telemetry(self, telemetry: dict) -> None:
        """ public method to persist telemetry object"""
