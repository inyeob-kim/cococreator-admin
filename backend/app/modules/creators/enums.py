from enum import StrEnum


class CreatorStatus(StrEnum):
    LEAD = "lead"
    CONTACTED = "contacted"
    NEGOTIATING = "negotiating"
    PARTNER = "partner"
    INACTIVE = "inactive"


class CreatorPlatform(StrEnum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class CreatorCategory(StrEnum):
    MUKBANG = "mukbang"
    FOOD = "food"
    BEAUTY = "beauty"
    FITNESS = "fitness"


class CreatorContactType(StrEnum):
    EMAIL = "email"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    MANAGER = "manager"

