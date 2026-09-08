from dataclasses import dataclass
from typing import Literal

FileID = str
UserID = str
ADMIN = "admin"


@dataclass
class File:
    size: int
    ownerID: UserID


@dataclass
class User:
    type: Literal["admin", "normal"]
    owned_files: set[str]
    max_capacity: int
    curr_capacity: int


class FileStorage:
    def __init__(self):
        self.files: dict[FileID, File] = {}
        admin = User("admin", set(), 0, 0)
        self.users: dict[UserID, User] = {"admin": admin}

    def add_file(self, name: str, size: int) -> bool:
        if name in self.files:
            return False

        self.files[name] = File(size, "admin")
        return True

    def get_file_size(self, name: str) -> int | None:
        if name not in self.files:
            return None

        return self.files[name].size

    def copy_file(self, src_file: str, dst_file: str) -> bool:
        if src_file not in self.files or dst_file in self.files:
            return False
        file = self.files[src_file]
        ownerID = file.ownerID
        owner = self.users[ownerID]
        if (
            owner.type == "admin"
            or owner.curr_capacity + file.size <= owner.max_capacity
        ):
            self.files[dst_file] = File(self.files[src_file].size, ownerID=ownerID)
            owner.owned_files.add(dst_file)
            owner.curr_capacity += file.size
            return True
        else:
            return False

    def find_files(self, prefix: str, suffix: str) -> list[str]:
        search_result = [
            (file_name, File)
            for file_name, File in self.files.items()
            if file_name.startswith(prefix) and file_name.endswith(suffix)
        ]
        search_result.sort(key=lambda file: (-file[1].size, file[0]))

        return [f"{file[0]}({file[1].size})" for file in search_result]

    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False

        self.users[user_id] = User(
            "normal",
            set(),
            max_capacity=capacity,
            curr_capacity=0,
        )
        return True

    def add_file_by(self, user_id: str, file_name: str, size: int) -> int | None:
        # ou o usuario não existe
        # ou o arquivo já tem dono obrigatóriamente
        user = self.users.get(user_id)
        if not user:
            return None
        if file_name in self.files:
            return None
        if size > user.max_capacity or user.curr_capacity + size > user.max_capacity:
            return None

        self.files[file_name] = File(size, ownerID=user_id)
        user.owned_files.add(file_name)
        user.curr_capacity += size
        return user.max_capacity - user.curr_capacity

    def update_capacity(self, user_id: str, new_cap: int) -> int | None:
        # find all owned files by user_id
        # remove on self.files by two params
        #   1. biggest file
        #   2. if equal, less lexi

        if user_id not in self.users:
            return None
        user = self.users[user_id]
        if user.type == "admin":
            return 0
        user.max_capacity = new_cap
        filtered_files = [
            (owned_file_name, self.files[owned_file_name])
            for owned_file_name in user.owned_files
        ]

        filtered_files.sort(key=lambda x: (-x[1].size, x[0]))
        removed_files = 0
        for file_name, file in filtered_files:
            if user.curr_capacity > user.max_capacity:
                del self.files[file_name]
                user.owned_files.discard(file_name)
                user.curr_capacity -= file.size
                removed_files += 1

        return removed_files

    def compress_file(self, user_id: str, file_name: str) -> int | None:
        compressed_file_name = f"{file_name}.COMPRESSED"
        user = self.users.get(user_id)
        file = self.files.get(file_name)

        if file_name.endswith(".COMPRESSED"):
            return None

        if not user:
            return None

        if not file:
            return None

        if file_name not in user.owned_files:
            return None

        if self.files.get(compressed_file_name):
            return None

        new_size = file.size // 2
        try_new_cap = user.curr_capacity - file.size
        if try_new_cap < 0:
            user.curr_capacity = 0
        else:
            user.curr_capacity = try_new_cap
        result = self.add_file_by(user_id, compressed_file_name, new_size)
        # Zero também indica sucesso: toda a capacidade foi utilizada.
        if result is not None:
            del self.files[file_name]
            user.owned_files.discard(file_name)
            return result
        else:
            user.curr_capacity += file.size
            return None

    def decompress_file(self, user_id: str, file_name: str) -> int | None:
        user = self.users.get(user_id)
        file = self.files.get(file_name)

        if not file_name.endswith(".COMPRESSED"):
            return None
        if not user or not file:
            return None
        if file_name not in user.owned_files:
            return None
        new_size = file.size * 2
        try_new_cap = user.curr_capacity - file.size
        if try_new_cap < 0:
            user.curr_capacity = 0
        else:
            user.curr_capacity = try_new_cap

        new_file_name = file_name[: len(file_name) - len(".COMPRESSED")]
        result = self.add_file_by(user_id, new_file_name, new_size)
        # Apenas None indica falha; zero é uma capacidade restante válida.
        if result is not None:
            del self.files[file_name]
            user.owned_files.discard(file_name)
            return result
        else:
            user.curr_capacity += file.size
            return None
