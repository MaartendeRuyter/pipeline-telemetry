"""Module to define abstract storage class
"""
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Any, Dict, Iterator

from ..data_classes import TelemetryData, TelemetryModel


class AbstractTelemetryStorage(metaclass=ABCMeta):
    """ Abstract Telemetry Storage class

    implements store_telemetry method that persists a given telemetry object

    Any class that stores the telemetry objects should be subclassed from
    this Abstract Class
    """
    __TELEMETRY_KEY: str = 'telemetry'

    @abstractmethod
    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """ public method to persist telemetry object"""

    @abstractmethod
    def select_records(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator:
        """
        Select telemetry records unique to a single process and source for as specific time period.
        """
        ...

    def _telemetry_storage_to_object(
            self, stored_telemetry_object: Dict) -> TelemetryModel:
        """Method to convert a sql light object into """
        telemetry_data = stored_telemetry_object.pop(
            self.__TELEMETRY_KEY, "{}")
        telemetry_model = TelemetryModel(**stored_telemetry_object)
        for sub_process, sub_process_tel_data in telemetry_data.items():
            telemetry_model.telemetry.update(
                {sub_process: TelemetryData(**sub_process_tel_data)}
            )

        return telemetry_model

    @staticmethod
    def _db_object_to_dict(db_object: Any) -> Dict:
        """Returns a db object as a dict object."""
        # If the persistance model does not return a proper Dict object then
        # override this method to ensure a Dict object is available.
        return db_object

    def telemetry_list(
            self, telemetry_type: str, category: str, sub_category: str,
            source_name: str, process_type: str, from_date_time: datetime,
            to_date_time: datetime) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a database query with the provided arguments.
        """
        selected_records = self.select_records(
            telemetry_type=telemetry_type, category=category,
            sub_category=sub_category, source_name=source_name,
            process_type=process_type, from_date_time=from_date_time,
            to_date_time=to_date_time
        )
        for record in selected_records:
            record_dict = self._db_object_to_dict(record)
            yield self._telemetry_storage_to_object(record_dict)
