CREATOR_TAG = "creators"

ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "lead": {"contacted", "inactive"},
    "contacted": {"negotiating", "inactive"},
    "negotiating": {"partner", "inactive"},
    "partner": {"inactive"},
    "inactive": set(),
}

ISO_COUNTRY_CODE_LEN = 2
