from enum import StrEnum


class PipelineStage(StrEnum):
    IDEA = "idea"
    RESEARCH = "research"
    SAMPLING = "sampling"
    OEM_NEGOTIATION = "oem_negotiation"
    PRODUCTION = "production"
    LAUNCH = "launch"
