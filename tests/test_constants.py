from svm_mms_common_utils.constants import MMS_CONSTANTS


def test_mms_constants():
    assert MMS_CONSTANTS.MAX_MRID_LENGTH == 35
    assert MMS_CONSTANTS.DECIMALS == 3
    assert MMS_CONSTANTS.PRICE_DECIMALS == 2
    assert MMS_CONSTANTS.TSOC_UUID == "10X1001A1001A523"
    assert MMS_CONSTANTS.DOMAIN_M_RID == "10YCY-1001A0003J"
