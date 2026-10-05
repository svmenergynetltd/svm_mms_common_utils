import datetime as dt

import pytest

from svm_mms_common_utils.enums import ResourceTypes
from svm_mms_common_utils.models.entities import MarketParticipant, ResourceObject


def _participant(**overrides) -> MarketParticipant:
    values = {
        "id": 4,
        "mRID": "10XPARTICIPANT",
        "participantName": "SVM Energy",
        "participantDisplayName": "SVM",
        "mainFunction": 1,
        "fmStrategy": 0.25,
        "managedBy": "ops",
        "mmsId": "mms-1",
        "dateAdded": dt.datetime(2024, 1, 15, 8, 30, 0),
        "dateModified": dt.datetime(2024, 2, 1, 9, 0, 0),
        "isActive": True,
    }
    values.update(overrides)
    return MarketParticipant(**values)


def _resource(**overrides) -> ResourceObject:
    values = {
        "id": 8,
        "name": "unit-a",
        "displayName": "Unit A",
        "mRID": "10XRESOURCE",
        "mmsId": "mms-res",
        "fmStrategy": 0.5,
        "damStrategy": "fixed",
        "damStrategyHolidays": "holiday",
        "rtbmStrategy": "variable",
        "rtbmStrategyHolidays": "rtbm-holiday",
        "rtbmBalEnergyOffers": "offers",
        "participantId": 4,
        "type": ResourceTypes.GENERATING_UNIT,
        "parentResourceId": 3,
    }
    values.update(overrides)
    return ResourceObject(**values)


def test_market_participant_to_db_formats_dates_and_active_flag():
    row = _participant().to_db()

    assert row == {
        "id": 4,
        "mRID": "10XPARTICIPANT",
        "participantName": "SVM Energy",
        "participantDisplayName": "SVM",
        "mainFunction": 1,
        "fmStrategy": 0.25,
        "managedBy": "ops",
        "mmsId": "mms-1",
        "dateAdded": "2024-01-15 08:30:00",
        "dateModified": "2024-02-01 09:00:00",
        "isActive": 1,
    }


def test_market_participant_to_db_allows_missing_dates_and_inactive_rows():
    row = _participant(dateAdded=None, dateModified=None, isActive=False).to_db()

    assert row["dateAdded"] is None
    assert row["dateModified"] is None
    assert row["isActive"] == 0


@pytest.mark.parametrize(
    ("stored", "expected"),
    [(1, True), (0, False), (True, True), (False, False)],
)
def test_market_participant_from_db(stored, expected):
    participant = MarketParticipant.from_db(
        {
            "id": 4,
            "mRID": "10XPARTICIPANT",
            "participantName": "SVM Energy",
            "participantDisplayName": "SVM",
            "mainFunction": 1,
            "fmStrategy": 0.25,
            "managedBy": "ops",
            "mmsId": "mms-1",
            "dateAdded": "2024-01-15 08:30:00",
            "dateModified": "2024-02-01 09:00:00",
            "isActive": stored,
        }
    )

    assert participant.isActive is expected
    assert participant.dateAdded == "2024-01-15 08:30:00"
    assert participant.mRID == "10XPARTICIPANT"
    assert participant.id == 4


def test_resource_object_to_db_stores_the_resource_type_value():
    row = _resource().to_db()

    assert row["type"] == "GENERATING_UNIT"
    assert row["parentResourceId"] == 3
    assert row["name"] == "unit-a"
    assert row["id"] == 8


def test_resource_object_from_db_restores_type_and_optional_parent():
    resource = ResourceObject.from_db(
        {
            "id": 8,
            "name": "unit-a",
            "displayName": "Unit A",
            "mRID": "10XRESOURCE",
            "mmsId": "mms-res",
            "fmStrategy": 0.5,
            "damStrategy": "fixed",
            "damStrategyHolidays": "holiday",
            "rtbmStrategy": "variable",
            "rtbmStrategyHolidays": "rtbm-holiday",
            "rtbmBalEnergyOffers": "offers",
            "participantId": 4,
            "type": "LOAD_UNIT",
        }
    )

    assert resource.type is ResourceTypes.LOAD_UNIT
    assert resource.parentResourceId is None


def test_resource_object_from_db_keeps_an_explicit_parent():
    payload = _resource().to_db()
    payload["type"] = "GENERATING_UNIT"

    restored = ResourceObject.from_db(payload)

    assert restored.type is ResourceTypes.GENERATING_UNIT
    assert restored.parentResourceId == 3
