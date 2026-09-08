from dataclasses import dataclass


@dataclass
class Account:
    balance: int = 0
    outgoing: int = 0


@dataclass
class PendingTransfer:
    source: str
    target: str
    amount: int
    deadline: int


class BankingSystem:
    TRANSFER_TTL = 86_400_000

    def __init__(self):
        self.accounts: dict[str, Account] = {}
        self.pending: dict[str, PendingTransfer] = {}
        self.next_transfer_id = 1

    def _expire_transfers(self, timestamp: int) -> None:
        # A snapshot lets us safely remove entries while iterating.
        for transfer_id, transfer in list(self.pending.items()):
            # Acceptance at the exact deadline is still valid.
            if timestamp > transfer.deadline:
                self.accounts[transfer.source].balance += transfer.amount
                del self.pending[transfer_id]

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._expire_transfers(timestamp)
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account()
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire_transfers(timestamp)
        account = self.accounts.get(account_id)
        if account is None:
            return None
        account.balance += amount
        return account.balance

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire_transfers(timestamp)
        account = self.accounts.get(account_id)
        if account is None or account.balance < amount:
            return None
        account.balance -= amount
        account.outgoing += amount
        return account.balance

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self._expire_transfers(timestamp)
        if n == 0:
            return []
        ranked = sorted(
            self.accounts,
            key=lambda account_id: (-self.accounts[account_id].outgoing, account_id),
        )
        return [
            f"{account_id}({self.accounts[account_id].outgoing})"
            for account_id in ranked[:n]
        ]

    def transfer(
        self, timestamp: int, source: str, target: str, amount: int
    ) -> str | None:
        self._expire_transfers(timestamp)
        if source == target or source not in self.accounts or target not in self.accounts:
            return None
        if self.accounts[source].balance < amount:
            return None

        transfer_id = f"transfer{self.next_transfer_id}"
        self.next_transfer_id += 1
        self.accounts[source].balance -= amount
        # Reserved money counts as outgoing only after acceptance.
        self.pending[transfer_id] = PendingTransfer(
            source, target, amount, timestamp + self.TRANSFER_TTL
        )
        return transfer_id

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        self._expire_transfers(timestamp)
        transfer = self.pending.get(transfer_id)
        if (
            account_id not in self.accounts
            or transfer is None
            or transfer.target != account_id
        ):
            return False

        self.accounts[account_id].balance += transfer.amount
        self.accounts[transfer.source].outgoing += transfer.amount
        # Removing completed transfers prevents double acceptance and refunds.
        del self.pending[transfer_id]
        return True

    def merge_accounts(self, timestamp: int, target: str, source: str) -> bool:
        self._expire_transfers(timestamp)
        if source == target or source not in self.accounts or target not in self.accounts:
            return False

        self.accounts[target].balance += self.accounts[source].balance
        self.accounts[target].outgoing += self.accounts[source].outgoing

        for transfer_id, transfer in list(self.pending.items()):
            if transfer.source == source:
                transfer.source = target
            if transfer.target == source:
                transfer.target = target

            if transfer.source == transfer.target:
                # The transfer is now internal: release its reserved money.
                self.accounts[target].balance += transfer.amount
                del self.pending[transfer_id]

        # All pending references have moved, so reusing this ID is safe.
        del self.accounts[source]
        return True
