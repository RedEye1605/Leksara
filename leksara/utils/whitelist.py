"""Whitelist tokens (e.g., [RATING], [PHONE])."""

DEFAULT_WHITELIST = {"[RATING]", "[PHONE]", "[EMAIL]", "[ADDRESS]", "[ID]"}
def protect_whitelist(x: str, whitelist=DEFAULT_WHITELIST):
    # bisa implement via placeholder sementara sebelum fungsi lain jalan
    ...
