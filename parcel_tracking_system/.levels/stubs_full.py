class ParcelTrackingSystem:
    def __init__(self):
        pass

    # Level 1
    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        raise NotImplementedError("Level 1: set_tag não implementado")

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        raise NotImplementedError("Level 1: get_tag não implementado")

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        raise NotImplementedError("Level 1: remove_tag não implementado")

    # Level 2
    def list_tags(self, parcel_id: str) -> list[str]:
        raise NotImplementedError("Level 2: list_tags não implementado")

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        raise NotImplementedError("Level 2: list_tags_by_prefix não implementado")

    # Level 3
    def set_tag_at(
        self, parcel_id: str, tag: str, value: str, timestamp: int
    ) -> None:
        raise NotImplementedError("Level 3: set_tag_at não implementado")

    def get_tag_at(
        self, parcel_id: str, tag: str, timestamp: int
    ) -> str | None:
        raise NotImplementedError("Level 3: get_tag_at não implementado")

    def remove_tag_at(
        self, parcel_id: str, tag: str, timestamp: int
    ) -> bool:
        raise NotImplementedError("Level 3: remove_tag_at não implementado")

    def set_tag_with_hold(
        self,
        parcel_id: str,
        tag: str,
        value: str,
        timestamp: int,
        ttl: int,
    ) -> None:
        raise NotImplementedError("Level 3: set_tag_with_hold não implementado")

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        raise NotImplementedError("Level 3: list_tags_at não implementado")

    def list_tags_by_prefix_at(
        self, parcel_id: str, prefix: str, timestamp: int
    ) -> list[str]:
        raise NotImplementedError(
            "Level 3: list_tags_by_prefix_at não implementado"
        )

    # Level 4
    def checkpoint(self, timestamp: int) -> int:
        raise NotImplementedError("Level 4: checkpoint não implementado")

    def restore_checkpoint(
        self, timestamp: int, timestamp_to_restore: int
    ) -> None:
        raise NotImplementedError("Level 4: restore_checkpoint não implementado")
