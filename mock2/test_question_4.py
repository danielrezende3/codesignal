import pytest
from mock2.solution import BankingSystem


def test_merge_accounts_basic_balance_and_outgoing_summation():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")

    bank.deposit(3, "A", 1000)
    bank.pay(4, "A", 300)  # A: balance=700, outgoing=300

    bank.deposit(5, "B", 600)
    bank.pay(6, "B", 200)  # B: balance=400, outgoing=200

    assert bank.merge_accounts(100, "A", "B") is True

    # B ceases to exist
    assert bank.deposit(101, "B", 100) is None
    assert bank.pay(102, "B", 100) is None

    # A has combined balance 700 + 400 = 1100 and outgoing 300 + 200 = 500
    assert bank.top_spenders(103, 5) == ["A(500)"]
    assert bank.pay(104, "A", 1100) == 0


def test_merge_accounts_validation_failures():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 500)

    # Same account merge
    assert bank.merge_accounts(4, "A", "A") is False

    # Missing target or source
    assert bank.merge_accounts(5, "A", "Missing") is False
    assert bank.merge_accounts(6, "Missing", "A") is False
    assert bank.merge_accounts(7, "Missing1", "Missing2") is False

    # Account state is preserved after failed merge
    assert bank.pay(8, "A", 500) == 0


def test_merged_source_account_deletion_subsequent_operations_fail():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")

    bank.deposit(4, "A", 500)
    bank.deposit(5, "B", 300)
    bank.deposit(6, "C", 200)

    assert bank.merge_accounts(7, "A", "B") is True

    # All operations targeting deleted account B must fail
    assert bank.deposit(8, "B", 100) is None
    assert bank.pay(9, "B", 50) is None
    assert bank.transfer(10, "B", "C", 50) is None
    assert bank.transfer(11, "C", "B", 50) is None
    assert bank.merge_accounts(12, "C", "B") is False
    assert bank.merge_accounts(13, "B", "C") is False
    assert bank.top_spenders(14, 5) == ["A(0)", "C(0)"]


def test_merge_pending_transfer_where_source_was_destination():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")

    bank.deposit(4, "C", 1000)

    # C transfers 400 to B
    tid = bank.transfer(5, "C", "B", 400)
    assert tid == "transfer1"

    # Merge B into A -> Transfer destination redirects from B to A (now C -> A)
    assert bank.merge_accounts(6, "A", "B") is True

    # Deleted account B cannot accept
    assert bank.accept_transfer(7, "B", "transfer1") is False

    # Target account A can accept
    assert bank.accept_transfer(8, "A", "transfer1") is True

    # Funds credited to A, outgoing credited to C
    assert bank.pay(9, "A", 400) == 0
    assert bank.pay(10, "C", 600) == 0
    assert bank.top_spenders(11, 2) == ["C(1000)", "A(400)"]


def test_merge_pending_transfer_where_source_was_origin():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")

    bank.deposit(4, "B", 1000)

    # B transfers 400 to C (B remaining balance = 600)
    tid = bank.transfer(5, "B", "C", 400)
    assert tid == "transfer1"

    # Merge B into A -> Transfer origin redirects from B to A (now A -> C)
    # A receives B's remaining balance of 600
    assert bank.merge_accounts(6, "A", "B") is True

    # C accepts transfer
    assert bank.accept_transfer(7, "C", "transfer1") is True

    # C balance = 400; A's outgoing increases by 400 (transfer) + 600 (pay) = 1000
    assert bank.pay(8, "C", 400) == 0
    assert bank.pay(9, "A", 600) == 0
    assert bank.top_spenders(10, 2) == ["A(1000)", "C(400)"]


def test_merge_pending_transfer_origin_redirection_and_expiration_refund():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")

    bank.deposit(4, "B", 1000)

    # B transfers 400 to C (B remaining balance = 600)
    tid = bank.transfer(5, "B", "C", 400)
    assert tid == "transfer1"

    # Merge B into A -> A receives 600
    assert bank.merge_accounts(6, "A", "B") is True

    # Transfer expires after 24h
    expire_time = 5 + 86_400_000 + 1
    assert bank.accept_transfer(expire_time, "C", "transfer1") is False

    # Expired transfer refund (400) goes to merged account A (A balance: 600 + 400 = 1000)
    assert bank.pay(expire_time + 1, "A", 1000) == 0
    assert bank.top_spenders(expire_time + 2, 2) == ["A(1000)", "C(0)"]


def test_merge_cancels_transfer_when_origin_and_target_become_equal():
    # Case 1: Transfer A -> B, then B merges into A (target A, source B)
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 1000)

    tid1 = bank.transfer(4, "A", "B", 400)  # A balance = 600
    assert tid1 == "transfer1"

    # B merges into A -> Transfer A -> B becomes A -> A
    # Must cancel transfer and refund 400 to A (A balance becomes 600 + 400 = 1000)
    assert bank.merge_accounts(5, "A", "B") is True
    assert bank.pay(6, "A", 1000) == 0
    # Transfer is cancelled and cannot be accepted
    assert bank.accept_transfer(7, "A", "transfer1") is False

    # Case 2: Transfer A -> B, then A merges into B (target B, source A)
    bank2 = BankingSystem()
    bank2.create_account(1, "A")
    bank2.create_account(2, "B")
    bank2.deposit(3, "A", 1000)

    tid2 = bank2.transfer(4, "A", "B", 400)  # A balance = 600
    assert tid2 == "transfer1"

    # A merges into B -> Transfer A -> B becomes B -> B
    # Must cancel transfer and refund 400 to resulting account B (B balance = 600 + 400 = 1000)
    assert bank2.merge_accounts(5, "B", "A") is True
    assert bank2.pay(6, "B", 1000) == 0
    assert bank2.accept_transfer(7, "B", "transfer1") is False


def test_merge_chained_and_multi_account_transfers():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")
    bank.create_account(4, "D")

    bank.deposit(5, "B", 500)

    # B transfers 300 to C (B balance = 200)
    tid = bank.transfer(6, "B", "C", 300)
    assert tid == "transfer1"

    # Chain merge: B into A (transfer becomes A -> C)
    assert bank.merge_accounts(7, "A", "B") is True

    # Chain merge: C into D (transfer becomes A -> D)
    assert bank.merge_accounts(8, "D", "C") is True

    # D accepts transfer from A
    assert bank.accept_transfer(9, "D", "transfer1") is True

    # D gets 300, A outgoing is 300, A balance is 200
    assert bank.pay(10, "D", 300) == 0
    assert bank.pay(11, "A", 200) == 0
    assert bank.top_spenders(12, 5) == [
        "A(500)",
        "D(300)",
    ]
