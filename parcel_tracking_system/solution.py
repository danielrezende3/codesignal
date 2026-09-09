class ParcelTrackingSystem:
    def __init__(self):
        pass

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        raise NotImplementedError("Level 1: set_tag não implementado")

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        raise NotImplementedError("Level 1: get_tag não implementado")

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        raise NotImplementedError("Level 1: remove_tag não implementado")
