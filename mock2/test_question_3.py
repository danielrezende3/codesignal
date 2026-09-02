import pytest
from mock2.solution import BankingSystem


def test_transfers_basic_and_immediate_withdrawal():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 1000)

    # Immediate balance deduction from source
    tid = bank.transfer(4, "A", "B", 400)
    assert tid == "transfer1"

    # A has 600 remaining; cannot pay 700, but can pay 600
    assert bank.pay(5, "A", 700) is None

    # Target B balance is NOT yet updated while transfer is pending
    assert bank.pay(6, "B", 100) is None

    # Source A outgoing is NOT counted yet while pending
    assert bank.top_spenders(7, 2) == ["A(0)", "B(0)"]

    # Target B accepts transfer
    assert bank.accept_transfer(8, "B", "transfer1") is True

    # Post-acceptance verification
    assert bank.pay(9, "B", 400) == 0
    assert bank.pay(10, "A", 600) == 0
    assert bank.top_spenders(11, 2) == ["A(1000)", "B(400)"]


def test_transfer_id_sequencing_only_on_success():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 500)

    # Failed transfers (insufficient funds, non-existent accounts, self-transfer)
    assert bank.transfer(4, "A", "B", 1000) is None       # Insufficient funds
    assert bank.transfer(5, "A", "Missing", 100) is None   # Target doesn't exist
    assert bank.transfer(6, "Missing", "B", 100) is None   # Source doesn't exist
    assert bank.transfer(7, "A", "A", 100) is None         # Self-transfer

    # First successful transfer must be "transfer1"
    tid1 = bank.transfer(8, "A", "B", 200)
    assert tid1 == "transfer1"

    # Another failed transfer must NOT advance the counter
    assert bank.transfer(9, "A", "B", 500) is None

    # Next successful transfer must be "transfer2"
    tid2 = bank.transfer(10, "A", "B", 100)
    assert tid2 == "transfer2"

    # Next successful transfer must be "transfer3"
    tid3 = bank.transfer(11, "A", "B", 200)
    assert tid3 == "transfer3"


def test_transfer_24h_exact_boundary_and_expiration():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")
    bank.deposit(4, "A", 2000)

    # Transfer 1 at t = 1000. 24h boundary is 1000 + 86_400_000 = 86401000
    tid1 = bank.transfer(1000, "A", "B", 500)
    assert tid1 == "transfer1"

    # Transfer 2 at t = 2000. 24h boundary + 1 ms is 2000 + 86_400_000 + 1 = 86402001
    tid2 = bank.transfer(2000, "A", "C", 700)
    assert tid2 == "transfer2"

    # A remaining balance = 2000 - 500 - 700 = 800

    # Acceptance at exact boundary (inclusive) must SUCCEED
    assert bank.accept_transfer(86401000, "B", "transfer1") is True
    assert bank.pay(86401001, "B", 500) == 0

    # Acceptance 1 unit past 24h boundary must FAIL (expired)
    assert bank.accept_transfer(86402001, "C", "transfer2") is False

    # Money from expired transfer2 (700) must be refunded to A
    # A balance: 800 + 700 = 1500
    assert bank.pay(86402002, "A", 1500) == 0

    # Attempting to accept an already expired transfer again must return False
    # and must NOT double refund to A
    assert bank.accept_transfer(86402003, "C", "transfer2") is False
    assert bank.pay(86402004, "A", 1) is None


def test_transfer_unauthorized_acceptance_and_double_acceptance():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")
    bank.deposit(4, "A", 1000)

    tid = bank.transfer(5, "A", "B", 400)
    assert tid == "transfer1"

    # Unauthorized accounts cannot accept (returns False, transfer remains pending)
    assert bank.accept_transfer(6, "C", "transfer1") is False
    assert bank.accept_transfer(7, "A", "transfer1") is False
    assert bank.accept_transfer(8, "Missing", "transfer1") is False

    # Legitimate target B accepts
    assert bank.accept_transfer(9, "B", "transfer1") is True

    # Cannot accept an already accepted transfer
    assert bank.accept_transfer(10, "B", "transfer1") is False
    assert bank.accept_transfer(11, "C", "transfer1") is False
    assert bank.accept_transfer(12, "A", "transfer1") is False


def test_transfer_invalid_transfer_id():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")

    assert bank.accept_transfer(3, "B", "transfer1") is False
    assert bank.accept_transfer(4, "B", "transfer999") is False
    assert bank.accept_transfer(5, "B", "invalid") is False


def test_multiple_concurrent_transfers_and_lifecycle():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")
    bank.deposit(4, "A", 1000)

    # A creates 2 pending transfers
    tid1 = bank.transfer(100, "A", "B", 300)  # A has 700
    tid2 = bank.transfer(200, "A", "C", 400)  # A has 300
    assert tid1 == "transfer1"
    assert tid2 == "transfer2"

    # A cannot transfer 400 (only 300 available)
    assert bank.transfer(300, "A", "B", 400) is None

    # A transfers remaining 300
    tid3 = bank.transfer(400, "A", "B", 300)  # A has 0
    assert tid3 == "transfer3"

    # B accepts transfer1 at t=500
    assert bank.accept_transfer(500, "B", "transfer1") is True

    # transfer2 expires (200 + 86_400_000 + 10)
    expire_time = 200 + 86_400_000 + 10
    assert bank.accept_transfer(expire_time, "C", "transfer2") is False

    # B accepts transfer3 within valid window
    assert bank.accept_transfer(expire_time + 1, "B", "transfer3") is True

    # A has 400 refunded from transfer2, B has 300+300=600, C has 0
    # A's outgoing is 300 + 300 = 600 (transfer1 + transfer3)
    # A pays 400 -> A outgoing = 1000
    # B pays 600 -> B outgoing = 600
    assert bank.pay(expire_time + 2, "A", 400) == 0
    assert bank.pay(expire_time + 3, "B", 600) == 0
    assert bank.top_spenders(expire_time + 4, 3) == [
        "A(1000)",
        "B(600)",
        "C(0)",
    ]
