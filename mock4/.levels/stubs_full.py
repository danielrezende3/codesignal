class BankingSystem:
    def __init__(self):
        pass

    # Level 1
    def create_account(self, timestamp: int, account_id: str) -> bool:
        raise NotImplementedError("Level 1: create_account não implementado")

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        raise NotImplementedError("Level 1: deposit não implementado")

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        raise NotImplementedError("Level 1: pay não implementado")

    # Level 2
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        raise NotImplementedError("Level 2: top_spenders não implementado")

    # Level 3
    def transfer(self, timestamp: int, source: str, target: str, amount: int) -> str | None:
        raise NotImplementedError("Level 3: transfer não implementado")

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        raise NotImplementedError("Level 3: accept_transfer não implementado")

    # Level 4
    def merge_accounts(self, timestamp: int, target: str, source: str) -> bool:
        raise NotImplementedError("Level 4: merge_accounts não implementado")
