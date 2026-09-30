from enum import Enum


class ResourceTypes(str, Enum):
    LOAD_UNIT = "LOAD_UNIT"
    GENERATING_UNIT = "GENERATING_UNIT"
