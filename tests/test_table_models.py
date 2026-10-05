import datetime as dt

import pytest

from svm_mms_common_utils.constants import MMS_CONSTANTS
from svm_mms_common_utils.enums import (
    ContractStatus,
    DamBidsOffersTypes,
    FmmqDocStatus,
    NominationType,
    NonAvailabilityReason,
    NonAvailabilityType,
    RtbmFlowDirection,
    RtbmReserveProcessType,
    SettlDocStatus,
    TransactionStatus,
    TrxSubmissionType,
)
from svm_mms_common_utils.models.tables import (
    MmsDamBidsOffers,
    MmsDamClearedEnergy,
    MmsDamClearingPrices,
    MmsDamExpectedGenMargin,
    MmsDamExpectedLoadMargin,
    MmsDamFcastedClearingPrices,
    MmsDamGenMargin,
    MmsForwardContract,
    MmsMarketSchedule,
    MmsParticipantFmmq,
    MmsPhysicalNomination,
    MmsResourceNonAvailability,
    MmsResourceObjectForecast,
    MmsRtbmBalancingEnergyOffers,
    MmsRtbmBeoAwards,
    MmsRtbmDispatch,
    MmsRtbmIndicativeDisp,
    MmsRtbmMargReservePrices,
    MmsRtbmMbep,
    MmsRtbmPlannedBEOActivations,
    MmsRtbmPlannedMbep,
    MmsRtbmReserveCapacityOffers,
    MmsSettlements,
    MmsTransactions,
)
from svm_mms_common_utils.models.tables.base_table_model import BaseTableModel
from svm_mms_common_utils.sql.sql_query import QueryType

DAY = dt.date(2024, 6, 15)
DAY_STR = "2024-06-15"
WHEN = dt.datetime(2024, 6, 15, 8, 30)
SERIES = [{"timestamp": "2024-06-15T00:00Z", "quantity": 1.5}]
EXPECTED_TABLES = {
    MmsDamBidsOffers: "MMS_DAM_BIDS_AND_OFFERS",
    MmsDamClearedEnergy: "MMS_DAM_CLEARED_ENERGY",
    MmsDamClearingPrices: "MMS_DAM_CLEARING_PRICES",
    MmsDamExpectedGenMargin: "MMS_DAM_EXPECTED_GEN_MARGIN",
    MmsDamExpectedLoadMargin: "MMS_DAM_EXPECTED_LOAD_MARGIN",
    MmsDamFcastedClearingPrices: "MMS_DAM_FORECASTED_CLEARING_PRICES",
    MmsDamGenMargin: "MMS_DAM_GEN_MARGIN",
    MmsForwardContract: "MMS_FORWARD_CONTRACTS",
    MmsMarketSchedule: "MMS_MARKET_SCHEDULE",
    MmsParticipantFmmq: "MMS_PARTICIPANT_FMMQ",
    MmsPhysicalNomination: "MMS_PHYSICAL_NOMINATIONS",
    MmsResourceNonAvailability: "MMS_RESOURCE_NON_AVAILABILITY",
    MmsResourceObjectForecast: "MMS_RESOURCE_OBJECT_FORECAST",
    MmsRtbmBalancingEnergyOffers: "MMS_RTBM_BALANCING_ENERGY_OFFERS",
    MmsRtbmBeoAwards: "MMS_RTBM_BEO_AWARDS",
    MmsRtbmDispatch: "MMS_RTBM_DISPATCH",
    MmsRtbmIndicativeDisp: "MMS_RTBM_INDICATIVE_DISP",
    MmsRtbmMargReservePrices: "MMS_RTBM_MARG_RESERVE_PRICES",
    MmsRtbmMbep: "MMS_RTBM_MBEP",
    MmsRtbmPlannedBEOActivations: "MMS_RTBM_PLANNED_BEO_ACTIVATION",
    MmsRtbmPlannedMbep: "MMS_RTBM_PLANNED_MBEP",
    MmsRtbmReserveCapacityOffers: "MMS_RTBM_RESERVE_CAPACITY_OFFERS",
    MmsSettlements: "MMS_SETTLEMENTS",
    MmsTransactions: "MMS_TRANSACTIONS",
}


def _rounded(value: float) -> float:
    return round(value, MMS_CONSTANTS.DECIMALS)


def _assert_insert(model):
    query = model.construct_query()
    sql = query.get_sql()

    assert query.queryType is QueryType.INSERT
    assert query.tableName == model.__tablename__
    assert query.valuesToInsert == [model.to_db()]
    assert sql.startswith(f"INSERT INTO {model.__tablename__} (")
    assert "VALUES" in sql
    return query


class _Unnamed(BaseTableModel):
    __tablename__ = None

    def to_db(self):
        return {"value": 1}


class _MissingTable(BaseTableModel):
    def to_db(self):
        return {"value": 1}


def test_base_table_model_methods_are_abstract():
    with pytest.raises(NotImplementedError):
        BaseTableModel.to_db(object())

    with pytest.raises(NotImplementedError):
        BaseTableModel.from_db({})


def test_construct_query_requires_a_table_name():
    with pytest.raises(NotImplementedError, match="Table name not defined"):
        _Unnamed().construct_query()

    with pytest.raises(AttributeError):
        _MissingTable().construct_query()


def test_table_names_are_unique_and_stable():
    assert {cls.__tablename__ for cls in EXPECTED_TABLES} == set(EXPECTED_TABLES.values())
    assert len(EXPECTED_TABLES) == len(set(EXPECTED_TABLES.values()))
    for cls, table_name in EXPECTED_TABLES.items():
        assert cls.__tablename__ == table_name


def _sample_models():
    pricing = {"strategy": "fixedPrice", "price": 12.5}
    return [
        MmsDamBidsOffers(
            id=1,
            resourceId=2,
            dayTimestamp=DAY,
            businessType=DamBidsOffersTypes["SIMPLE_OFFER"],
            totalQuantity=1.23456,
            quantities=SERIES,
            pricingStrategy=pricing,
            createdBy="bids-user",
            pricesCreatedBy="price-user",
        ),
        MmsDamClearedEnergy(
            resourceId=2,
            dayTimestamp=DAY_STR,
            clearedEnergy=SERIES,
            totalBoughtEnergy=1.23456,
            totalSoldEnergy=2.5,
            id=3,
        ),
        MmsDamClearingPrices(dayTimestamp=DAY_STR, clearingPrices=SERIES, id=4),
        MmsDamExpectedGenMargin(
            resourceId=2,
            dayTimestamp=DAY_STR,
            totalMargin=3.4567,
            damMargin=SERIES,
            id=5,
        ),
        MmsDamExpectedLoadMargin(
            resourceId=2,
            dayTimestamp=DAY_STR,
            totalMargin=3.4567,
            damMargin=SERIES,
            id=6,
        ),
        MmsDamFcastedClearingPrices(
            dayTimestamp=DAY_STR,
            forecastedClearingPrices=SERIES,
            id=7,
        ),
        MmsDamGenMargin(
            dayTimestamp=DAY_STR,
            resourceId=2,
            totalMargin=3.4567,
            damMargin=SERIES,
            id=8,
        ),
        MmsForwardContract(
            id=9,
            inParticipantId=1,
            outParticipantId=2,
            marketAgreementMRID="AGR-1",
            dayTimestamp=DAY,
            forwardContract=SERIES,
            totalDayEnergy=4.3219,
            status=ContractStatus["CONFIRMED"],
            createdBy="fm-user",
        ),
        MmsMarketSchedule(
            id=10,
            resourceId=2,
            dayTimestamp=DAY_STR,
            totalScheduledEnergy=8.1,
            marketSchedule=SERIES,
        ),
        MmsParticipantFmmq(
            participantId=1,
            dayTimestamp=DAY_STR,
            documentStatus=FmmqDocStatus["FINAL"],
            fmmqTimeseries=SERIES,
            totalFMMQ=1.23456,
            averageFMMQ=0.3336,
            id=11,
            xmlFile="<xml/>",
        ),
        MmsPhysicalNomination(
            id=12,
            dayTimestamp=DAY,
            resourceId=2,
            nomination=SERIES,
            totalDayEnergy=6.7891,
            energyFlow=NominationType["DELIVERY"],
            createdBy="nom-user",
        ),
        MmsResourceNonAvailability(
            id=13,
            resourceId=2,
            startDate=WHEN,
            endDate=WHEN,
            nonAvailability=0.4,
            reason=NonAvailabilityReason["B18"],
            type=NonAvailabilityType["PARTIAL_Z01"],
            status="OPEN",
        ),
        MmsResourceObjectForecast(
            id=14,
            resourceId=2,
            dayTimestamp=DAY,
            forecast=SERIES,
            subunitForecast=SERIES,
            totalDayImportEnergy=1.23456,
            totalDayExportEnergy=2.34567,
            createdBy="forecast-user",
        ),
        MmsRtbmBalancingEnergyOffers(
            id=15,
            resourceId=2,
            dayTimestamp=WHEN,
            flowDirection=RtbmFlowDirection["UP"],
            totalQuantity=1.23456,
            quantities=SERIES,
            pricingStrategy=pricing,
            createdBy="beo-user",
            pricesCreatedBy="beo-price",
        ),
        MmsRtbmBeoAwards(
            id=16,
            resourceId=2,
            dayTimestamp=DAY_STR,
            flowDirection=RtbmFlowDirection["DOWN"],
            totalQuantity=9.87654,
            balancingEnergy=SERIES,
        ),
        MmsRtbmDispatch(
            id=17,
            resourceId=2,
            dayTimestamp=DAY_STR,
            dispatchInstructions=SERIES,
        ),
        MmsRtbmIndicativeDisp(
            id=18,
            resourceId=2,
            dayTimestamp=DAY_STR,
            indicativeDispSchedule=SERIES,
        ),
        MmsRtbmMargReservePrices(
            dayTimestamp=DAY_STR,
            processType=RtbmReserveProcessType["aFRR"],
            marginalReservePrices=SERIES,
            id=19,
        ),
        MmsRtbmMbep(dayTimestamp=DAY_STR, pricesMbep=SERIES, id=20),
        MmsRtbmPlannedBEOActivations(
            id=21,
            resourceId=2,
            dayTimestamp=DAY_STR,
            flowDirection=RtbmFlowDirection["UP"],
            totalQuantity=5.5555,
            balancingEnergy=SERIES,
        ),
        MmsRtbmPlannedMbep(dayTimestamp=DAY_STR, pricesPlannedMbep=SERIES, id=22),
        MmsRtbmReserveCapacityOffers(
            id=23,
            resourceId=2,
            dayTimestamp=DAY_STR,
            processType=RtbmReserveProcessType["mFRR"],
            flowDirection=RtbmFlowDirection["DOWN"],
            totalQuantity=7.8912,
            quantities=SERIES,
            pricingStrategy=pricing,
            createdBy="reserve-user",
            pricesCreatedBy="reserve-price",
        ),
        MmsSettlements(
            id=24,
            dayTimestamp=DAY,
            participantId=1,
            resourceId=2,
            documentMRID="DOC-1",
            timeseriesMRID="TS-1",
            documentStatus=SettlDocStatus["INTERMEDIATE"],
            resolution="PT30M",
            statementType="STATEMENT",
            businessType="B01",
            data=SERIES,
        ),
        MmsTransactions(
            id=25,
            submissionType=TrxSubmissionType["DAM_BIDS"],
            participantId=1,
            resourceObjectId=2,
            marketDay=DAY,
            scheduledDateTime=WHEN,
            status=TransactionStatus["SUBMITTED"],
            mRID="TRX-1",
            revision=3,
            databaseRowId=99,
            databaseTableName="MMS_DAM_BIDS_AND_OFFERS",
            xmlFile="file.xml",
            sentXml="<sent/>",
            receivedXml="<received/>",
            dateSent=WHEN,
            dateReceived=WHEN,
            timeSeries=SERIES,
            dateAdded="2024-06-15 08:00:00",
            dateUpdated=WHEN,
        ),
    ]


@pytest.mark.parametrize("model", _sample_models(), ids=lambda model: type(model).__name__)
def test_every_table_model_builds_an_insert_for_its_row(model):
    assert type(model) in EXPECTED_TABLES
    _assert_insert(model)


def test_dam_bids_offers_round_trip():
    model = _sample_models()[0]
    row = model.to_db()

    assert row["dayTimestamp"] == DAY_STR
    assert row["totalQuantity"] == _rounded(1.23456)
    assert row["businessType"] == DamBidsOffersTypes["SIMPLE_OFFER"]
    assert "id" not in row

    restored = MmsDamBidsOffers.from_db(
        {**row, "id": 1, "dayTimestamp": DAY, "businessType": "SIMPLE_OFFER"}
    )

    assert restored.id == 1
    assert restored.businessType == DamBidsOffersTypes.SIMPLE_OFFER
    assert restored.quantities == SERIES

    with pytest.raises(KeyError):
        MmsDamBidsOffers.from_db({**row, "id": 1, "businessType": "MISSING"})


def test_dam_bids_offers_formats_a_missing_day_as_none():
    model = MmsDamBidsOffers(
        id=None,
        resourceId=2,
        dayTimestamp=None,
        businessType=DamBidsOffersTypes["SIMPLE_BIDS"],
        totalQuantity=0,
        quantities=[],
        pricingStrategy={},
        createdBy="bids-user",
        pricesCreatedBy="price-user",
    )

    assert model.to_db()["dayTimestamp"] is None
    assert model.to_db()["totalQuantity"] == 0


@pytest.mark.parametrize(
    "cls",
    [MmsDamGenMargin, MmsDamExpectedGenMargin, MmsDamExpectedLoadMargin],
)
def test_dam_margin_models_round_the_total_and_allow_a_missing_id(cls):
    payload = {
        "dayTimestamp": DAY_STR,
        "resourceId": 2,
        "totalMargin": 3.4567,
        "damMargin": SERIES,
    }

    restored = cls.from_db(payload)
    row = restored.to_db()

    assert restored.id is None
    assert row["totalMargin"] == _rounded(3.4567)
    assert row["damMargin"] is SERIES
    assert row["dayTimestamp"] == DAY_STR


def test_dam_cleared_energy_rounds_bought_and_sold_totals():
    model = MmsDamClearedEnergy(
        resourceId=2,
        dayTimestamp=DAY_STR,
        clearedEnergy=SERIES,
        totalBoughtEnergy=1.23444,
        totalSoldEnergy=1.23456,
    )

    row = model.to_db()
    restored = MmsDamClearedEnergy.from_db(row)

    assert row["totalBoughtEnergy"] == _rounded(1.23444)
    assert row["totalSoldEnergy"] == _rounded(1.23456)
    assert restored.id is None
    assert restored.clearedEnergy == SERIES


@pytest.mark.parametrize(
    ("cls", "field"),
    [
        (MmsDamClearingPrices, "clearingPrices"),
        (MmsDamFcastedClearingPrices, "forecastedClearingPrices"),
    ],
)
def test_dam_price_models_pass_series_through(cls, field):
    model = cls(dayTimestamp=DAY_STR, **{field: SERIES})
    row = model.to_db()

    assert row == {"dayTimestamp": DAY_STR, field: SERIES}
    assert cls.from_db(row).id is None
    assert getattr(cls.from_db({**row, "id": 4}), field) == SERIES


def test_forward_contract_formats_the_day_and_restores_status():
    model = next(model for model in _sample_models() if isinstance(model, MmsForwardContract))
    row = model.to_db()

    assert row["dayTimestamp"] == DAY_STR
    assert row["totalDayEnergy"] == _rounded(4.3219)
    assert row["status"] == ContractStatus["CONFIRMED"]

    restored = MmsForwardContract.from_db(
        {**row, "id": 9, "dayTimestamp": DAY, "status": "CONFIRMED"}
    )

    assert restored.status == ContractStatus.CONFIRMED
    assert restored.marketAgreementMRID == "AGR-1"


def test_market_schedule_rounds_scheduled_energy():
    model = MmsMarketSchedule(
        id=10,
        resourceId=2,
        dayTimestamp=DAY_STR,
        totalScheduledEnergy=8.12345,
        marketSchedule=SERIES,
    )

    assert model.to_db()["totalScheduledEnergy"] == _rounded(8.12345)
    assert "id" not in model.to_db()

    restored = MmsMarketSchedule.from_db({**model.to_db(), "id": 10})
    assert restored.marketSchedule == SERIES
    assert restored.resourceId == 2


def test_participant_fmmq_rounds_totals_and_reads_optional_xml():
    model = MmsParticipantFmmq(
        participantId=1,
        dayTimestamp=DAY_STR,
        documentStatus=FmmqDocStatus["INTERMEDIATE"],
        fmmqTimeseries=SERIES,
        totalFMMQ=1.23456,
        averageFMMQ=0.3336,
    )
    row = model.to_db()

    assert row["totalFMMQ"] == _rounded(1.23456)
    assert row["averageFMMQ"] == _rounded(0.3336)
    assert row["xmlFile"] is None
    assert row["documentStatus"] == FmmqDocStatus["INTERMEDIATE"]

    restored = MmsParticipantFmmq.from_db({**row, "documentStatus": "FINAL"})
    assert restored.id is None
    assert restored.xmlFile is None
    assert restored.documentStatus == FmmqDocStatus.FINAL


def test_physical_nomination_formats_optional_day_and_energy_flow():
    model = MmsPhysicalNomination(
        id=12,
        dayTimestamp=None,
        resourceId=2,
        nomination=SERIES,
        totalDayEnergy=6.7891,
        energyFlow=NominationType["OFFTAKE"],
        createdBy="nom-user",
    )
    row = model.to_db()

    assert row["dayTimestamp"] is None
    assert row["totalDayEnergy"] == _rounded(6.7891)
    assert row["energyFlow"] == NominationType["OFFTAKE"]

    restored = MmsPhysicalNomination.from_db(
        {**row, "id": 12, "dayTimestamp": DAY, "energyFlow": "DELIVERY"}
    )
    assert restored.energyFlow == NominationType.DELIVERY


def test_resource_non_availability_serializes_dates_and_looks_up_type_by_name():
    model = MmsResourceNonAvailability(
        id=13,
        resourceId=2,
        startDate=WHEN,
        endDate=None,
        nonAvailability=0.4,
        reason=NonAvailabilityReason["Z05"],
        type=NonAvailabilityType["TOTAL_Z02"],
        status=None,
    )
    row = model.to_db()

    assert row["startDate"] == WHEN.isoformat()
    assert row["endDate"] is None
    assert row["nonAvailability"] == 0.4
    assert row["reason"] == NonAvailabilityReason["Z05"]
    assert row["type"] == NonAvailabilityType["TOTAL_Z02"]

    restored = MmsResourceNonAvailability.from_db(
        {
            "id": 13,
            "resourceId": 2,
            "startDate": WHEN,
            "endDate": WHEN,
            "nonAvailability": 0.4,
            "type": "PARTIAL_Z01",
            "reason": "B19",
        }
    )
    assert isinstance(restored.type, NonAvailabilityType)
    assert restored.type.name == "PARTIAL_Z01"
    assert restored.reason == NonAvailabilityReason.B19
    assert restored.status is None

    unknown = MmsResourceNonAvailability.from_db(
        {
            "id": 13,
            "resourceId": 2,
            "startDate": WHEN,
            "endDate": WHEN,
            "nonAvailability": 0.4,
            "type": "Z01",
            "reason": "B18",
            "status": "CLOSED",
        }
    )
    assert unknown.type is None
    assert unknown.status == "CLOSED"


def test_resource_forecast_rounds_import_and_export_and_formats_the_day():
    model = MmsResourceObjectForecast(
        id=14,
        resourceId=2,
        dayTimestamp=None,
        forecast=SERIES,
        subunitForecast=[],
        totalDayImportEnergy=1.23456,
        totalDayExportEnergy=2.34567,
        createdBy="forecast-user",
    )
    row = model.to_db()

    assert row["dayTimestamp"] is None
    assert row["totalDayImportEnergy"] == _rounded(1.23456)
    assert row["totalDayExportEnergy"] == _rounded(2.34567)

    restored = MmsResourceObjectForecast.from_db({**row, "id": 14, "dayTimestamp": DAY})
    assert restored.subunitForecast == []
    assert restored.createdBy == "forecast-user"


def test_balancing_energy_offers_format_only_datetime_days():
    model = MmsRtbmBalancingEnergyOffers(
        id=15,
        resourceId=2,
        dayTimestamp=WHEN,
        flowDirection=RtbmFlowDirection["UP"],
        totalQuantity=1.23456,
        quantities=SERIES,
        pricingStrategy={"strategy": "fixedPrice"},
        createdBy="beo-user",
        pricesCreatedBy="beo-price",
    )

    assert model.to_db()["dayTimestamp"] == DAY_STR
    assert model.to_db()["totalQuantity"] == _rounded(1.23456)
    assert model.to_db()["flowDirection"] == RtbmFlowDirection["UP"]

    for day in (DAY_STR, DAY, None):
        model.dayTimestamp = day
        assert model.to_db()["dayTimestamp"] is None

    restored = MmsRtbmBalancingEnergyOffers.from_db(
        {
            **model.to_db(),
            "id": 15,
            "dayTimestamp": DAY_STR,
            "flowDirection": "DOWN",
        }
    )
    assert restored.flowDirection == RtbmFlowDirection.DOWN
    assert restored.dayTimestamp == DAY_STR


@pytest.mark.parametrize(
    "cls",
    [MmsRtbmBeoAwards, MmsRtbmPlannedBEOActivations],
)
def test_balancing_energy_award_models(cls):
    model = cls(
        id=16,
        resourceId=2,
        dayTimestamp=DAY_STR,
        flowDirection=RtbmFlowDirection["DOWN"],
        totalQuantity=9.87654,
        balancingEnergy=SERIES,
    )
    row = model.to_db()

    assert row["totalQuantity"] == _rounded(9.87654)
    assert row["flowDirection"] == RtbmFlowDirection["DOWN"]
    assert "id" not in row

    restored = cls.from_db({**row, "id": 16, "flowDirection": "UP"})
    assert restored.flowDirection == RtbmFlowDirection.UP
    assert restored.balancingEnergy == SERIES


@pytest.mark.parametrize(
    ("cls", "field"),
    [
        (MmsRtbmDispatch, "dispatchInstructions"),
        (MmsRtbmIndicativeDisp, "indicativeDispSchedule"),
    ],
)
def test_dispatch_models_pass_instructions_through(cls, field):
    model = cls(id=17, resourceId=2, dayTimestamp=DAY_STR, **{field: SERIES})
    row = model.to_db()

    assert row == {"resourceId": 2, "dayTimestamp": DAY_STR, field: SERIES}
    restored = cls.from_db({**row, "id": 17})
    assert getattr(restored, field) == SERIES
    assert restored.resourceId == 2


def test_marginal_reserve_prices_restore_process_type():
    model = MmsRtbmMargReservePrices(
        dayTimestamp=DAY_STR,
        processType=RtbmReserveProcessType["FCR"],
        marginalReservePrices=SERIES,
    )
    row = model.to_db()

    assert row == {
        "dayTimestamp": DAY_STR,
        "processType": RtbmReserveProcessType["FCR"],
        "marginalReservePrices": SERIES,
    }
    restored = MmsRtbmMargReservePrices.from_db({**row, "processType": "aFRR"})
    assert restored.id is None
    assert restored.processType == RtbmReserveProcessType.aFRR


@pytest.mark.parametrize(
    ("cls", "field"),
    [
        (MmsRtbmMbep, "pricesMbep"),
        (MmsRtbmPlannedMbep, "pricesPlannedMbep"),
    ],
)
def test_mbep_models_pass_prices_through(cls, field):
    model = cls(dayTimestamp=DAY_STR, **{field: SERIES})
    row = model.to_db()

    assert row == {"dayTimestamp": DAY_STR, field: SERIES}
    assert cls.from_db(row).id is None
    assert getattr(cls.from_db({**row, "id": 20}), field) == SERIES


def test_reserve_capacity_offers_keep_process_and_flow():
    model = MmsRtbmReserveCapacityOffers(
        id=23,
        resourceId=2,
        dayTimestamp=DAY_STR,
        processType=RtbmReserveProcessType["mFRR"],
        flowDirection=RtbmFlowDirection["UP"],
        totalQuantity=7.89123,
        quantities=SERIES,
        pricingStrategy={"strategy": "variablePrice"},
        createdBy="reserve-user",
        pricesCreatedBy="reserve-price",
    )
    row = model.to_db()

    assert row["totalQuantity"] == _rounded(7.89123)
    assert row["processType"] == RtbmReserveProcessType["mFRR"]
    assert row["flowDirection"] == RtbmFlowDirection["UP"]

    restored = MmsRtbmReserveCapacityOffers.from_db(
        {**row, "id": 23, "processType": "FCR", "flowDirection": "DOWN"}
    )
    assert restored.processType == RtbmReserveProcessType.FCR
    assert restored.flowDirection == RtbmFlowDirection.DOWN


def test_settlements_format_the_day_and_restore_document_status():
    model = MmsSettlements(
        id=24,
        dayTimestamp=DAY,
        participantId=1,
        resourceId=2,
        documentMRID="DOC-1",
        timeseriesMRID="TS-1",
        documentStatus=SettlDocStatus["FINAL"],
        resolution="PT30M",
        statementType="STATEMENT",
        businessType="B01",
        data=SERIES,
    )
    row = model.to_db()

    assert row["dayTimestamp"] == DAY_STR
    assert row["documentStatus"] == SettlDocStatus["FINAL"]
    assert row["data"] is SERIES

    restored = MmsSettlements.from_db(
        {**row, "id": 24, "dayTimestamp": DAY, "documentStatus": "UNKNOWN"}
    )
    assert restored.documentStatus == SettlDocStatus.UNKNOWN
    assert restored.statementType == "STATEMENT"


def test_transactions_format_dates_and_omit_identity_columns():
    model = MmsTransactions(
        id=25,
        submissionType=TrxSubmissionType["RTBM_BE_OFFER"],
        participantId=1,
        resourceObjectId=2,
        marketDay=DAY,
        scheduledDateTime=WHEN,
        status=TransactionStatus["REJECT_GATE_CLOSED"],
        mRID="TRX-1",
        databaseRowId=99,
        databaseTableName="MMS_RTBM_BALANCING_ENERGY_OFFERS",
        xmlFile="file.xml",
        sentXml="<sent/>",
        receivedXml="<received/>",
        dateSent=WHEN,
        dateReceived=None,
        timeSeries=SERIES,
        dateAdded="2024-06-15 08:00:00",
        dateUpdated=WHEN,
    )
    row = model.to_db()

    assert row["marketDay"] == DAY_STR
    assert row["scheduledDateTime"] == "2024-06-15 08:30:00"
    assert row["dateSent"] == "2024-06-15 08:30:00"
    assert row["dateReceived"] is None
    assert row["revision"] == 1
    assert row["status"] == TransactionStatus["REJECT_GATE_CLOSED"]
    assert row["submissionType"] == TrxSubmissionType["RTBM_BE_OFFER"]
    assert "id" not in row
    assert "dateUpdated" not in row

    restored = MmsTransactions.from_db(
        {
            **row,
            "id": 25,
            "status": "CONFIRMED",
            "submissionType": "FM_CONTRACT",
            "marketDay": DAY,
            "scheduledDateTime": WHEN,
            "dateSent": None,
            "dateReceived": WHEN,
            "dateUpdated": WHEN,
        }
    )
    assert restored.status == TransactionStatus.CONFIRMED
    assert restored.submissionType == TrxSubmissionType.FM_CONTRACT
    assert restored.dateUpdated == WHEN
    assert restored.timeSeries == SERIES


def test_transactions_allow_missing_optional_dates():
    model = MmsTransactions(
        id=None,
        submissionType=TrxSubmissionType["FETCH_MBEP"],
        participantId=1,
        resourceObjectId=None,
        marketDay=None,
        scheduledDateTime=None,
        status=TransactionStatus["PENDING"],
    )
    row = model.to_db()

    assert row["marketDay"] is None
    assert row["scheduledDateTime"] is None
    assert row["dateSent"] is None
    assert row["dateReceived"] is None
    assert row["mRID"] is None
    assert row["timeSeries"] is None
    assert row["dateAdded"]


def test_transactions_share_the_class_default_date_added():
    first = MmsTransactions(
        id=1,
        submissionType=TrxSubmissionType["DAM_OFFERS"],
        participantId=1,
        resourceObjectId=2,
        marketDay=DAY,
        scheduledDateTime=WHEN,
        status=TransactionStatus["PENDING"],
    )
    second = MmsTransactions(
        id=2,
        submissionType=TrxSubmissionType["DAM_OFFERS"],
        participantId=1,
        resourceObjectId=2,
        marketDay=DAY,
        scheduledDateTime=WHEN,
        status=TransactionStatus["PENDING"],
    )

    assert first.dateAdded == second.dateAdded
    assert first.revision == 1
