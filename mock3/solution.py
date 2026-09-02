class InMemoryDB:
    def __init__(self):
        pass

    # Level 1
    def set(self, timestamp: int, key: str, field: str, value: int) -> None:
        raise NotImplementedError("Level 1: set não implementado")

    def get(self, timestamp: int, key: str, field: str) -> int | None:
        raise NotImplementedError("Level 1: get não implementado")

    def delete(self, timestamp: int, key: str, field: str) -> bool:
        raise NotImplementedError("Level 1: delete não implementado")

    # Level 2
    def scan(self, timestamp: int, key: str) -> list[str]:
        raise NotImplementedError("Level 2: scan não implementado")

    def scan_by_prefix(self, timestamp: int, key: str, prefix: str) -> list[str]:
        raise NotImplementedError("Level 2: scan_by_prefix não implementado")

    # Level 3
    def set_with_ttl(self, timestamp: int, key: str, field: str, value: int, ttl: int) -> None:
        raise NotImplementedError("Level 3: set_with_ttl não implementado")

    # Level 4
    def get_at(self, timestamp: int, key: str, field: str, at_timestamp: int) -> int | None:
        raise NotImplementedError("Level 4: get_at não implementado")
