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
>>> aggregated_telemetry = aggregator.aggregate(telemetry_queryset)

"""

from abc import ABC
from datetime import date, datetime, timedelta
from typing import Iterator, Protocol, Type

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.settings.date_ranges import DateTimeRange, get_daily_date_ranges

from .helper import TelemetryAggregator, TelemetryListArgs, TelemetrySelector

DATE_TIME_RANGE_GENERATOR = {
    st.DAILY_AGGR_TELEMETRY_TYPE: get_daily_date_ranges,
}


class TelemetryStorage(Protocol):
    def telemetry_list(
        self,
        telemetry_type: str,
        category: str,
        sub_category: str,
        source_name: str,
        process_type: str,
        from_date_time: datetime,
        to_date_time: datetime,
    ) -> Iterator[TelemetryModel]:
        """
        Method to return an iteraror TelemetryModel instances retrieved from a
        database query with the provided arguments.
        """
        ...

    def store_telemetry(self, telemetry: TelemetryModel) -> None:
        """public method to persist telemetry object"""
        ...


class AbstractAggregator(ABC):
    """
    Aggregator to aggregate all SINGLE TELEMETRY objects for a single day
    into a telemetry objetc of type DAILY AGGREGATION.

    When initializig the class a TelemetrySelector should provided that
    determine which telemnetry objects are in scope

    The following methods are available to run the actual aggregations

    - aggregate: Method to implememt the aggregation
    """

    FROM_TELEMETRY_TYPE: str
    TO_TELEMETRY_TYPE: str

    __telemetry_selector: TelemetrySelector
    __target_telemetry: TelemetryModel
    __telemetry_storage: TelemetryStorage
    __aggregator: Type[TelemetryAggregator] = TelemetryAggregator

    def __init__(
        self, telemetry_selector: TelemetrySelector, telemetry_storage: TelemetryStorage
    ) -> None:
        self.__telemetry_selector = telemetry_selector
        self.__telemetry_storage = telemetry_storage
        self._set_target_telemetry_model()

    @property
    def target_telemetry(self):
        return self.__target_telemetry

    @property
    def storage_class(self):
        return self.__telemetry_storage

    def aggregate(self, start_date: date, end_date: date) -> None:
        """Method to run all aggregations in the given time period."""
        date_time_ranges = self._get_date_ranges(
            start_date=start_date, end_date=end_date
        )
        for date_time_range in date_time_ranges:
            aggregated_telemetry = self._run_aggregation(date_time_range)
            self.__telemetry_storage.store_telemetry(aggregated_telemetry)

    def _get_date_ranges(
        self, start_date: date, end_date: date
    ) -> Iterator[DateTimeRange]:
        """
        Method to return the list of date ranges based upon start and end
        date.
        """
        generator = DATE_TIME_RANGE_GENERATOR.get(self.TO_TELEMETRY_TYPE)
        if not generator:
            raise exceptions.UnknownTelemetryType(self.TO_TELEMETRY_TYPE)

        return generator(start_date=start_date, end_date=end_date)

    def _run_aggregation(self, date_time_range: DateTimeRange) -> TelemetryModel:
        """
        Method to run the actual aggregation and return the aggregated telemetry model.
        """
        # gather the database instances to be aggregated
        telemetry_list_params = self._telememtry_list_params(date_time_range)._asdict()
        telemetry_objects = self.__telemetry_storage.telemetry_list(
            **telemetry_list_params
        )

        initial_telemetry_obj = self.__target_telemetry.copy()
        aggregator = self.__aggregator(initial_telemetry_obj)
        aggregated_telemetry = aggregator.aggregate(telemetry_objects)

        return self._set_start_date_time_for_aggregated_telemetry(
            aggregated_telemetry, date_time_range
        )

    @staticmethod
    def _set_start_date_time_for_aggregated_telemetry(
        telemetry_obj: TelemetryModel, date_time_range: DateTimeRange
    ) -> TelemetryModel:
        """
        Method to set the telemetry start_date_time attribute to the date_time
        for which the aggregation was run as start_date_time is set to now() by
        default.
        """
        # For daily telemetry aggregation the date of the aggregated object
        # is the from_date attribute in the date_time_range
        telemetry_obj.start_date_time = date_time_range.from_date
        return telemetry_obj

    def _set_target_telemetry_model(self) -> None:
        """
        Method to create and set the initial instance of the target telemetry
        model.
        """
        self.__target_telemetry = TelemetryModel(
            telemetry_type=self.TO_TELEMETRY_TYPE,
            source_name=self.__telemetry_selector.source_name,
            process_type=self.__telemetry_selector.process_type,
            category=self.__telemetry_selector.category,
            sub_category=self.__telemetry_selector.sub_category,
        )

    def _telememtry_list_params(
        self, date_time_range: DateTimeRange
    ) -> TelemetryListArgs:
        """
        Method to return telemetry_list_params that can be used to retrieve a
        list of TelemetryModel objects from the storage model.

        i.e. these params serve as input to the telemetry_list method of the
        storage_class
        """
        telemetry_list_params = self.__telemetry_selector._asdict()
        return TelemetryListArgs(
            telemetry_type=self.FROM_TELEMETRY_TYPE,
            from_date_time=date_time_range.from_date,
            to_date_time=date_time_range.to_date,
            **telemetry_list_params,
        )


class DailyAggregator(AbstractAggregator):
    """
    Aggregator to aggregate all SINGLE TELEMETRY objects for a single day
    into a telemetry objetc of type DAILY AGGREGATION.

    When initializig the class a TelemetrySelector should provided that
    determine which telemnetry objects are in scope

    The following methods are available to run the actual aggregations

    - aggregate: makes daily aggregations from start_date to end_date
    - aggregate_yesterday: makes daily aggregation for yesterday
    """

    FROM_TELEMETRY_TYPE = st.SINGLE_TELEMETRY_TYPE
    TO_TELEMETRY_TYPE = st.DAILY_AGGR_TELEMETRY_TYPE

    def aggregate_yesterday(self) -> None:
        """Method to run the aggregation for yesterday."""
        start_date = date.today()
        end_date = date.today() - timedelta(days=1)
        self.aggregate(start_date=start_date, end_date=end_date)


class PartialToSingleAggregator(AbstractAggregator):
    """
    Aggregator to aggregate all PARTIAL TELEMETRY objects for a single day
    into a telemetry objetc of type SINGLE AGGREGATION.

    When initializig the class a TelemetrySelector should provided that
    determine which telemnetry objects are in scope

    The following methods are available to run the actual aggregations

    - aggregate: makes daily aggregations from start_date to end_date
    """

    FROM_TELEMETRY_TYPE = st.PARTIAL_AGGR_TELEMETRY_TYPE
    TO_TELEMETRY_TYPE = st.SINGLE_TELEMETRY_TYPE
