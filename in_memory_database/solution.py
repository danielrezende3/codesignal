from bisect import bisect_right
from dataclasses import dataclass
from operator import attrgetter


@dataclass(frozen=True)
class Version:
    timestamp: int
    value: int | None
    expires_at: int | None = None


class InMemoryDB:
    def __init__(self) -> None:
        self.history: dict[str, dict[str, list[Version]]] = {}

    def _write(self, key: str, field: str, version: Version) -> None:
        versions = self.history.setdefault(key, {}).setdefault(field, [])
        # Calls arrive chronologically; equal timestamps retain call order.
        versions.append(version)

    def _value_at(self, timestamp: int, key: str, field: str) -> int | None:
        versions = self.history.get(key, {}).get(field, [])
        index = bisect_right(versions, timestamp, key=attrgetter("timestamp")) - 1
        if index < 0:
            return None

        version = versions[index]
        # Only the latest version at this time matters. Never fall back to an
        # older version when this one has expired or represents a deletion.
        if version.expires_at is not None and timestamp >= version.expires_at:
            return None
        return version.value

    def set(self, timestamp: int, key: str, field: str, value: int) -> None:
        self._write(key, field, Version(timestamp, value))

    def get(self, timestamp: int, key: str, field: str) -> int | None:
        return self._value_at(timestamp, key, field)

    def delete(self, timestamp: int, key: str, field: str) -> bool:
        if self._value_at(timestamp, key, field) is None:
            return False
        # A tombstone records deletion without destroying historical values.
        self._write(key, field, Version(timestamp, None))
        return True

    def scan(self, timestamp: int, key: str) -> list[str]:
        return self.scan_by_prefix(timestamp, key, "")

    def scan_by_prefix(self, timestamp: int, key: str, prefix: str) -> list[str]:
        result = []
        for field in sorted(self.history.get(key, {})):
            if field.startswith(prefix):
                value = self._value_at(timestamp, key, field)
                if value is not None:
                    result.append(f"{field}({value})")
        return result

    def set_with_ttl(
        self, timestamp: int, key: str, field: str, value: int, ttl: int
    ) -> None:
        self._write(key, field, Version(timestamp, value, timestamp + ttl))

    def get_at(
        self, timestamp: int, key: str, field: str, at_timestamp: int
    ) -> int | None:
        # timestamp is the call time; at_timestamp is the time being queried.
        return self._value_at(at_timestamp, key, field)
