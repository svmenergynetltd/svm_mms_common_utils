from enum import Enum


class MridMarketAbbr(str, Enum):
    forwardMarket = "FM"
    dayAheadMarket = "DAM"
    balancingMarket = "BM"


class TsocDocType(str, Enum):
    nonAvailabilityDeclaration = "NAD"
    technoEconomicDeclaration = "TED"
    damEnergyOrdersDocument = "RBM"
    rrqnReplacementReserveQuantitiesNominations = "RRQN"
    pdonAndPsutcNominationDocument = "PDON"
    forwardContractNominations = "FCN"
    rrBidDocument = "BIDRR"
    crBidDocument = "BIDCR"
    bsBidDocument = "BIDBS"
    balancingEnergyOffer = "BEO"
    balancingReserveCapacityOffers = "BRCO"
    forecastMarketParticipantResInjection = "FORMPRESI"
    netDeliveryPositionReport = "NDP"
    forwardMarketMismatchReport = "FMMQ"
    rrAuctionSpecificationDocument = "RRAUCSPEC"
    bsAuctionSpecificationDocument = "BSAUCSPEC"
    crAuctionSpecificationDocument = "CRAUCSPEC"
    bsAwardedBidDocument = "AWBIDBS"
    crAwardedBidDocument = "AWBIDCR"
    rrAwardedBidDocument = "AWBIDRR"
    anomalyReport = "ANO"
    confirmationsOfNominationsReport = "CONF"
    marketClearingPriceForecasts = "MCPF"
    marketClearingPrices = "MCP"
    clearedEnergyVolumesAndPrices = "CEVP"
    marketSchedules = "MS"
    commitmentSchedules = "COMMSHED"
    reserveAwards = "RESAWAR"
    marginalReservePrices = "MARRESPRI"
    indicativeDispatchSchedules = "IDISPSCHED"
    plannedActivationOfBalancingEnergyOffers = "PABEO"
    plannedMarginalBalancingEnergyPrices = "PMARBEPRI"
    prospectivePayments = "PRP"
    balancingEnergyOfferAwards = "BEOA"
    marginalBalancingEnergyPrices = "MBEP"
    dispatchInstructions = "DISP"
    statementDocument = "STAT"
    noticeDocument = "NOTICE"
