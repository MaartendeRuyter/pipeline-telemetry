from pipeline_telemetry import ProcessType, ProcessTypes, ProcessTypesMeta

FLOW_1 = [
    "GET_DATA_RESPONSES",
    "STORE_DATA",
]

FLOW_2 = [
    "GET_DATA_RESPONSES",
    "CONVERT_DATA",
]


class TestTypesOne:
    """
    Class to define the process types with their subtypes for Wearther module
    """

    FLOW_ONE = ProcessType(process_type="F1", subtypes=FLOW_1)


class TestTypesTwo:
    """
    Class to define the process types with their subtypes for Wearther module
    """

    FLOW_TWO = ProcessType(process_type="F2", subtypes=FLOW_2)

    NO_PROCESS_TYPE: str = "other attribute"


def test_process_type_meta_exists():
    assert ProcessTypesMeta


def test_meta_class_adds_process_types_to_registered_list():
    class NewClass(TestTypesOne, TestTypesTwo, metaclass=ProcessTypesMeta): ...  # noqa: E701

    # assert NewClass.is_registered(TestTypesOne.FLOW_ONE)
    assert NewClass.is_registered(TestTypesTwo.FLOW_TWO)


def test_meta_class_skips_non_process_types_attributes():
    class NewClass(TestTypesOne, TestTypesTwo, metaclass=ProcessTypesMeta): ...  # noqa: E701

    assert hasattr(TestTypesTwo, "NO_PROCESS_TYPE")
    assert not NewClass.is_registered(TestTypesTwo.NO_PROCESS_TYPE)  # type: ignore


def test_class_from_metaclass_issubclass_process_types_class():
    class NewClass(TestTypesOne, TestTypesTwo, metaclass=ProcessTypesMeta): ...  # noqa: E701

    assert issubclass(NewClass, ProcessTypes)
