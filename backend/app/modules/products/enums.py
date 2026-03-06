from enum import StrEnum


class ProductStatus(StrEnum):
    IDEA = "idea"
    RESEARCH = "research"
    SAMPLING = "sampling"
    OEM_NEGOTIATION = "oem_negotiation"
    PRODUCTION = "production"
    LAUNCH = "launch"
    ACTIVE = "active"
    PAUSED = "paused"
