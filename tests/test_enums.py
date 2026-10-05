import pytest

from svm_mms_common_utils.enums import (
    ContractStatus,
    DamBidsOffersTypes,
    DamPricingStrategyTypes,
    FmmqDocStatus,
    MridMarketAbbr,
    NominationType,
    NonAvailabilityReason,
    NonAvailabilityType,
    PowerUnits,
    ResourceTypes,
    RtbmFlowDirection,
    RtbmPricingStrategyTypes,
    RtbmReserveProcessType,
    SettlDocStatus,
    TransactionStatus,
    TrxSubmissionType,
    TsocDocType,
)


def test_base_enum_attribute_access_returns_the_value():
    assert DamBidsOffersTypes.SIMPLE_BIDS == "SIMPLE_BIDS"
    assert type(DamBidsOffersTypes.SIMPLE_BIDS) is str

    member = DamBidsOffersTypes.__members__["SIMPLE_BIDS"]
    assert isinstance(member, DamBidsOffersTypes)
    assert member.value == "SIMPLE_BIDS"
    assert DamBidsOffersTypes["SIMPLE_BIDS"] is member


@pytest.mark.parametrize(
    ("enum_cls", "expected"),
    [
        (
            DamBidsOffersTypes,
            {
                "SIMPLE_BIDS": "SIMPLE_BIDS",
                "SIMPLE_OFFER": "SIMPLE_OFFER",
                "BLOCK_OFFER": "BLOCK_OFFER",
            },
        ),
        (
            DamPricingStrategyTypes,
            {
                "FIXED_PRICE": "fixedPrice",
                "VARIABLE_PRICE": "variablePrice",
                "STEP_OFFERS": "stepOffers",
                "BLOCK_OFFERS": "blockOffers",
            },
        ),
        (
            NominationType,
            {"OFFTAKE": "OFFTAKE", "DELIVERY": "DELIVERY"},
        ),
        (
            ContractStatus,
            {
                "PENDING": "PENDING",
                "ACKNOWLEDGED": "ACKNOWLEDGED",
                "CONFIRMED": "CONFIRMED",
                "ANOMALY_DETECTED": "ANOMALY_DETECTED",
                "SELF_CONTRACT": "SELF_CONTRACT",
                "SUBMIT_FAILED": "SUBMIT_FAILED",
                "MUST_RUN": "MUST_RUN",
            },
        ),
        (
            FmmqDocStatus,
            {"INTERMEDIATE": "INTERMEDIATE", "FINAL": "FINAL", "UNKNOWN": "UNKNOWN"},
        ),
        (RtbmFlowDirection, {"UP": "UP", "DOWN": "DOWN"}),
        (
            RtbmReserveProcessType,
            {"FCR": "FCR", "aFRR": "aFRR", "mFRR": "mFRR"},
        ),
        (
            RtbmPricingStrategyTypes,
            {"FIXED_PRICE": "fixedPrice", "VARIABLE_PRICE": "variablePrice"},
        ),
        (
            SettlDocStatus,
            {"INTERMEDIATE": "INTERMEDIATE", "FINAL": "FINAL", "UNKNOWN": "UNKNOWN"},
        ),
        (
            NonAvailabilityType,
            {"PARTIAL_Z01": "Z01", "TOTAL_Z02": "Z02", "CANCEL_Z03": "Z03"},
        ),
        (
            NonAvailabilityReason,
            {
                "B18": "B18",
                "B19": "B19",
                "B20": "B20",
                "A95": "A95",
                "Z01": "Z01",
                "Z02": "Z02",
                "Z03": "Z03",
                "Z04": "Z04",
                "Z05": "Z05",
                "Z06": "Z06",
            },
        ),
        (
            TransactionStatus,
            {
                "PENDING": "PENDING",
                "SUBMITTED": "SUBMITTED",
                "CONFIRMED": "CONFIRMED",
                "ACCEPTED_WITH_WARNINGS": "ACCEPTED_WITH_WARNINGS",
                "FAILED": "FAILED",
                "REJECTED": "REJECTED",
                "REJECT_GATE_CLOSED": "REJECT_GATE_CLOSED",
            },
        ),
        (
            TrxSubmissionType,
            {
                "FETCH_MARKET_SCHEDULE": "FETCH_MARKET_SCHEDULE",
                "FETCH_CLEARING_PRICES": "FETCH_CLEARING_PRICES",
                "FETCH_FCAST_CLEARING_PRICES": "FETCH_FCAST_CLEARING_PRICES",
                "FETCH_DAM_MARGIN": "FETCH_DAM_MARGIN",
                "FETCH_DAM_CLEARED_ENERGY": "FETCH_DAM_CLEARED_ENERGY",
                "FM_CONTRACT": "FM_CONTRACT",
                "FM_NOMINATION": "FM_NOMINATION",
                "DAM_BIDS": "DAM_BIDS",
                "DAM_OFFERS": "DAM_OFFERS",
                "RES_INJECTION": "RES_INJECTION",
                "FETCH_PLANNED_MBEP": "FETCH_PLANNED_MBEP",
                "FETCH_MBEP": "FETCH_MBEP",
                "FETCH_IND_DISP": "FETCH_IND_DISP",
                "FETCH_DISP": "FETCH_DISP",
                "FETCH_PLANNED_ABEO": "FETCH_PLANNED_ABEO",
                "FETCH_ABEO": "FETCH_ABEO",
                "FETCH_FMMQ": "FETCH_FMMQ",
                "FETCH_MARG_RESERVE_PRICES": "FETCH_MARG_RESERVE_PRICES",
                "RTBM_BE_OFFER": "RTBM_BE_OFFER",
                "RTBM_RESERVE_CAP_OFFER": "RTBM_RESERVE_CAP_OFFER",
                "TE_NONAVAILABILITY": "TE_NONAVAILABILITY",
            },
        ),
    ],
)
def test_base_enum_members(enum_cls, expected):
    assert {member.name: member.value for member in enum_cls} == expected
    for name, value in expected.items():
        assert enum_cls[name].value == value
        assert enum_cls(value).name == name
        assert getattr(enum_cls, name) == value


@pytest.mark.parametrize(
    ("enum_cls", "expected"),
    [
        (ResourceTypes, {"LOAD_UNIT": "LOAD_UNIT", "GENERATING_UNIT": "GENERATING_UNIT"}),
        (PowerUnits, {"MWH": "MWH", "KWH": "KWH", "MW": "MW", "KW": "KW"}),
        (
            MridMarketAbbr,
            {
                "forwardMarket": "FM",
                "dayAheadMarket": "DAM",
                "balancingMarket": "BM",
            },
        ),
        (
            TsocDocType,
            {
                "nonAvailabilityDeclaration": "NAD",
                "technoEconomicDeclaration": "TED",
                "damEnergyOrdersDocument": "RBM",
                "rrqnReplacementReserveQuantitiesNominations": "RRQN",
                "pdonAndPsutcNominationDocument": "PDON",
                "forwardContractNominations": "FCN",
                "rrBidDocument": "BIDRR",
                "crBidDocument": "BIDCR",
                "bsBidDocument": "BIDBS",
                "balancingEnergyOffer": "BEO",
                "balancingReserveCapacityOffers": "BRCO",
                "forecastMarketParticipantResInjection": "FORMPRESI",
                "netDeliveryPositionReport": "NDP",
                "forwardMarketMismatchReport": "FMMQ",
                "rrAuctionSpecificationDocument": "RRAUCSPEC",
                "bsAuctionSpecificationDocument": "BSAUCSPEC",
                "crAuctionSpecificationDocument": "CRAUCSPEC",
                "bsAwardedBidDocument": "AWBIDBS",
                "crAwardedBidDocument": "AWBIDCR",
                "rrAwardedBidDocument": "AWBIDRR",
                "anomalyReport": "ANO",
                "confirmationsOfNominationsReport": "CONF",
                "marketClearingPriceForecasts": "MCPF",
                "marketClearingPrices": "MCP",
                "clearedEnergyVolumesAndPrices": "CEVP",
                "marketSchedules": "MS",
                "commitmentSchedules": "COMMSHED",
                "reserveAwards": "RESAWAR",
                "marginalReservePrices": "MARRESPRI",
                "indicativeDispatchSchedules": "IDISPSCHED",
                "plannedActivationOfBalancingEnergyOffers": "PABEO",
                "plannedMarginalBalancingEnergyPrices": "PMARBEPRI",
                "prospectivePayments": "PRP",
                "balancingEnergyOfferAwards": "BEOA",
                "marginalBalancingEnergyPrices": "MBEP",
                "dispatchInstructions": "DISP",
                "statementDocument": "STAT",
                "noticeDocument": "NOTICE",
            },
        ),
    ],
)
def test_plain_str_enums_keep_member_on_attribute_access(enum_cls, expected):
    assert {member.name: member.value for member in enum_cls} == expected
    for name, value in expected.items():
        member = getattr(enum_cls, name)
        assert isinstance(member, enum_cls)
        assert member.value == value
        assert enum_cls(value) is member


@pytest.mark.parametrize(
    ("code", "expected"),
    [("A47", "mFRR"), ("A51", "aFRR"), ("A52", "FCR"), ("UNKNOWN", None)],
)
def test_reserve_process_from_process_code(code, expected):
    assert RtbmReserveProcessType.from_process_code(code) == expected


@pytest.mark.parametrize(
    ("code", "expected"),
    [("A95", "FCR"), ("A96", "aFRR"), ("A97", "mFRR"), ("UNKNOWN", None)],
)
def test_reserve_process_from_business_code(code, expected):
    assert RtbmReserveProcessType.from_business_code(code) == expected


def test_non_availability_type_from_name():
    partial = NonAvailabilityType.from_name("PARTIAL_Z01")
    assert isinstance(partial, NonAvailabilityType)
    assert partial.name == "PARTIAL_Z01"
    assert partial.value == "Z01"
    assert partial == NonAvailabilityType.PARTIAL_Z01

    assert NonAvailabilityType.from_name("TOTAL_Z02").value == "Z02"
    assert NonAvailabilityType.from_name("CANCEL_Z03").value == "Z03"
    assert NonAvailabilityType.from_name("Z01") is None
    assert NonAvailabilityType.from_name(None) is None
    assert NonAvailabilityType.from_name("MISSING") is None
