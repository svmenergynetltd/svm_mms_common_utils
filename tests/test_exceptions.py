import pytest

from svm_mms_common_utils.exceptions.mms import MMS_Fetch_Empty_Response, MMS_Fetch_Error


@pytest.mark.parametrize(
    "exc_type",
    [MMS_Fetch_Error, MMS_Fetch_Empty_Response],
)
def test_mms_exceptions_expose_message(exc_type):
    error = exc_type("market fetch failed")

    assert isinstance(error, Exception)
    assert error.message == "market fetch failed"
    assert str(error) == "market fetch failed"
    assert error.args == ("market fetch failed",)


def test_mms_exceptions_are_distinct_types():
    assert not issubclass(MMS_Fetch_Error, MMS_Fetch_Empty_Response)
    assert not issubclass(MMS_Fetch_Empty_Response, MMS_Fetch_Error)
