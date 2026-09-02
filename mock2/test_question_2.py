import pytest
from mock2.solution import BankingSystem


def test_top_spenders_basic():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")

    bank.deposit(4, "A", 1000)
    bank.deposit(5, "B", 1000)
    bank.deposit(6, "C", 1000)

    bank.pay(7, "A", 500)
    bank.pay(8, "B", 900)
    bank.pay(9, "C", 500)

    # B: 900, A: 500, C: 500 -> A before C because of alphabetical tie-break
    assert bank.top_spenders(100, 3) == [
        "B(900)",
        "A(500)",
        "C(500)",
    ]


def test_top_spenders_zero_outgoing_and_tie_breaking():
    bank = BankingSystem()
    bank.create_account(1, "zeta")
    bank.create_account(2, "beta")
    bank.create_account(3, "alpha")

    # All accounts have 0 outgoing; must be sorted alphabetically
    assert bank.top_spenders(4, 3) == [
        "alpha(0)",
        "beta(0)",
        "zeta(0)",
    ]
    assert bank.top_spenders(5, 2) == [
        "alpha(0)",
        "beta(0)",
    ]
    assert bank.top_spenders(6, 1) == [
        "alpha(0)",
    ]


def test_top_spenders_n_boundary_conditions():
    bank = BankingSystem()
    # Empty bank returns empty list
    assert bank.top_spenders(1, 0) == []
    assert bank.top_spenders(2, 5) == []

    bank.create_account(3, "acc1")
    bank.create_account(4, "acc2")
    bank.create_account(5, "acc3")

    bank.deposit(6, "acc1", 500)
    bank.pay(7, "acc1", 100)

    # N = 0
    assert bank.top_spenders(8, 0) == []

    # N smaller than total accounts
    assert bank.top_spenders(9, 2) == [
        "acc1(100)",
        "acc2(0)",
    ]

    # N equal to total accounts
    assert bank.top_spenders(10, 3) == [
        "acc1(100)",
        "acc2(0)",
        "acc3(0)",
    ]

    # N larger than total accounts (should return all accounts without error/padding)
    assert bank.top_spenders(11, 100) == [
        "acc1(100)",
        "acc2(0)",
        "acc3(0)",
    ]


def test_top_spenders_deposits_and_failed_pays_do_not_count():
    bank = BankingSystem()
    bank.create_account(1, "rich_saver")
    bank.create_account(2, "failed_buyer")
    bank.create_account(3, "frugal_spender")

    # rich_saver deposits large amount, never pays -> outgoing = 0
    bank.deposit(4, "rich_saver", 1_000_000)

    # failed_buyer deposits 100, attempts to pay 200 (fails) -> outgoing = 0
    bank.deposit(5, "failed_buyer", 100)
    assert bank.pay(6, "failed_buyer", 200) is None

    # frugal_spender deposits 50, pays 10 -> outgoing = 10
    bank.deposit(7, "frugal_spender", 50)
    assert bank.pay(8, "frugal_spender", 10) == 40

    assert bank.top_spenders(9, 3) == [
        "frugal_spender(10)",
        "failed_buyer(0)",
        "rich_saver(0)",
    ]


def test_top_spenders_multi_tier_tie_breaking():
    bank = BankingSystem()
    for acc in ["dave", "charlie", "bob", "alice", "eve"]:
        bank.create_account(1, acc)
        bank.deposit(2, acc, 2000)

    # Tier 1 (1000 spent): bob, alice
    bank.pay(3, "bob", 1000)
    bank.pay(4, "alice", 1000)

    # Tier 2 (500 spent): dave, charlie
    bank.pay(5, "dave", 500)
    bank.pay(6, "charlie", 500)

    # Tier 3 (0 spent): eve

    assert bank.top_spenders(10, 5) == [
        "alice(1000)",
        "bob(1000)",
        "charlie(500)",
        "dave(500)",
        "eve(0)",
    ]
    assert bank.top_spenders(11, 3) == [
        "alice(1000)",
        "bob(1000)",
        "charlie(500)",
    ]


def test_top_spenders_cumulative_spending_progression():
    bank = BankingSystem()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 1000)
    bank.deposit(4, "B", 1000)

    # Initial state
    assert bank.top_spenders(5, 2) == ["A(0)", "B(0)"]

    # A pays 100 -> A leads
    bank.pay(6, "A", 100)
    assert bank.top_spenders(7, 2) == ["A(100)", "B(0)"]

    # B pays 200 -> B leads
    bank.pay(8, "B", 200)
    assert bank.top_spenders(9, 2) == ["B(200)", "A(100)"]

    # A pays 300 more -> A total 400, takes lead back
    bank.pay(10, "A", 300)
    assert bank.top_spenders(11, 2) == ["A(400)", "B(200)"]

    # B pays 200 more -> B total 400, ties A; A wins alphabetically
    bank.pay(12, "B", 200)
    assert bank.top_spenders(13, 2) == ["A(400)", "B(400)"]
