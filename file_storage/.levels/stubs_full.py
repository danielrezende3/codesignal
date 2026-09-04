class FileStorage:
    def __init__(self):
        pass

    # Level 1
    def add_file(self, name: str, size: int) -> bool:
        raise NotImplementedError("Level 1: add_file não implementado")

    def get_file_size(self, name: str) -> int | None:
        raise NotImplementedError("Level 1: get_file_size não implementado")

    def copy_file(self, source: str, destination: str) -> bool:
        raise NotImplementedError("Level 1: copy_file não implementado")

    # Level 2
    def find_files(self, prefix: str, suffix: str) -> list[str]:
        raise NotImplementedError("Level 2: find_files não implementado")

    # Level 3
    def add_user(self, user_id: str, capacity: int) -> bool:
        raise NotImplementedError("Level 3: add_user não implementado")

    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        raise NotImplementedError("Level 3: add_file_by não implementado")

    def update_capacity(self, user_id: str, capacity: int) -> int | None:
        raise NotImplementedError("Level 3: update_capacity não implementado")

    # Level 4
    def compress_file(self, user_id: str, name: str) -> int | None:
        raise NotImplementedError("Level 4: compress_file não implementado")

    def decompress_file(self, user_id: str, name: str) -> int | None:
        raise NotImplementedError("Level 4: decompress_file não implementado")
