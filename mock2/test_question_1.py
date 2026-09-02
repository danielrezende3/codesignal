import pytest
from mock2.solution import BankingSystem


def test_account_creation_basic_and_duplicate_prevention():
    bank = BankingSystem()
    # Create valid accounts
    assert bank.create_account(1, "A") is True
    assert bank.create_account(2, "B") is True
    assert bank.create_account(3, "user_123") is True

    # Duplicate account creation must return False
    assert bank.create_account(4, "A") is False
    assert bank.create_account(5, "B") is False
    assert bank.create_account(6, "user_123") is False


def test_duplicate_creation_does_not_reset_account_state():
    bank = BankingSystem()
    assert bank.create_account(1, "A") is True
    assert bank.deposit(2, "A", 1000) == 1000

    # Attempting to re-create account A should return False and keep existing balance intact
    assert bank.create_account(3, "A") is False
    assert bank.deposit(4, "A", 500) == 1500
    assert bank.pay(5, "A", 1500) == 0


def test_deposit_operations_and_non_existent_accounts():
    bank = BankingSystem()
    bank.create_account(1, "A")

    # Initial balance is 0, deposit updates and returns new balance
    assert bank.deposit(2, "A", 100) == 100
    assert bank.deposit(3, "A", 250) == 350
    assert bank.deposit(4, "A", 650) == 1000

    # Deposit to non-existent account returns None and does not create the account
    assert bank.deposit(5, "non_existent", 500) is None
    assert bank.deposit(6, "Missing", 100) is None
    assert bank.pay(7, "non_existent", 50) is None


def test_pay_operations_insufficient_balance_and_exact_zero():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.deposit(2, "A", 1000)

    # Partial payment
    assert bank.pay(3, "A", 300) == 700

    # Insufficient balance returns None and preserves balance
    assert bank.pay(4, "A", 800) is None
    assert bank.pay(5, "A", 701) is None

    # Pay exact balance succeeds and leaves exactly 0
    assert bank.pay(6, "A", 700) == 0

    # Pay on 0 balance returns None
    assert bank.pay(7, "A", 1) is None
    assert bank.pay(8, "A", 100) is None

    # Pay on non-existent account returns None
    assert bank.pay(9, "Ghost", 50) is None


def test_chronological_interleaved_deposits_and_payments():
    bank = BankingSystem()
    bank.create_account(1, "acc1")
    bank.create_account(2, "acc2")

    # Operations on acc1
    assert bank.deposit(3, "acc1", 500) == 500
    assert bank.pay(4, "acc1", 200) == 300
    assert bank.deposit(5, "acc1", 700) == 1000
    assert bank.pay(6, "acc1", 1000) == 0

    # Operations on acc2
    assert bank.pay(7, "acc2", 100) is None
    assert bank.deposit(8, "acc2", 300) == 300
    assert bank.deposit(9, "acc2", 200) == 500
    assert bank.pay(10, "acc2", 400) == 100

    # Verify acc1 still 0 and acc2 still 100
    assert bank.pay(11, "acc1", 1) is None
    assert bank.pay(12, "acc2", 100) == 0


def test_account_isolation():
    bank = BankingSystem()
    bank.create_account(1, "alice")
    bank.create_account(2, "bob")

    assert bank.deposit(3, "alice", 1000) == 1000
    # bob balance is still 0
    assert bank.pay(4, "bob", 100) is None
    assert bank.pay(5, "alice", 400) == 600

    assert bank.deposit(6, "bob", 500) == 500
    assert bank.pay(7, "alice", 600) == 0
    assert bank.pay(8, "bob", 500) == 0
