CODES = {
    "E_NOT_FOUND",
    "E_UNKNOWN_CUSTOMER",
    "E_BAD_ZONE",
    "E_BAD_WEIGHT",
    "E_BAD_STATE",
    "E_BAD_INPUT",
    "E_LIMIT",
}


class DomainError(Exception):
    def __init__(self, code, message=""):
        if code not in CODES:
            raise RuntimeError(f"unregistered error code {code}")
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
