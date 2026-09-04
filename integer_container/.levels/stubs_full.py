class IntegerContainer:
    def __init__(self):
        pass

    # Level 1
    def add(self, value: int) -> int:
        raise NotImplementedError("Level 1: add não implementado")

    def delete(self, value: int) -> bool:
        raise NotImplementedError("Level 1: delete não implementado")

    # Level 2
    def get_median(self) -> int | None:
        raise NotImplementedError("Level 2: get_median não implementado")
