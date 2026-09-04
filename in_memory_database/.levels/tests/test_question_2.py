from in_memory_database.solution import InMemoryDB


def test_scan_and_scan_by_prefix_basic():
    db = InMemoryDB()
    db.set(1, "user1", "age", 26)
    db.set(2, "user1", "address", 10)
    db.set(3, "user1", "score", 100)

    assert db.scan(10, "user1") == [
        "address(10)",
        "age(26)",
        "score(100)",
    ]

    assert db.scan_by_prefix(10, "user1", "a") == [
        "address(10)",
        "age(26)",
    ]

    assert db.scan_by_prefix(10, "user1", "z") == []
    assert db.scan(10, "missing_user") == []
    assert db.scan_by_prefix(10, "missing_user", "a") == []


def test_scan_sorting_and_deleted_fields():
    db = InMemoryDB()
    db.set(1, "rec", "beta", 2)
    db.set(2, "rec", "alpha", 1)
    db.set(3, "rec", "gamma", 3)
    db.set(4, "rec", "delta", 4)

    db.delete(5, "rec", "beta")

    assert db.scan(6, "rec") == [
        "alpha(1)",
        "delta(4)",
        "gamma(3)",
    ]


def test_scan_empty_prefix_matches_all():
    db = InMemoryDB()
    db.set(1, "rec", "b", 2)
    db.set(2, "rec", "a", 1)

    assert db.scan_by_prefix(3, "rec", "") == [
        "a(1)",
        "b(2)",
    ]


def test_scan_by_prefix_does_not_match_prefix_in_the_middle():
    db = InMemoryDB()
    db.set(1, "rec", "banana", 1)
    db.set(2, "rec", "nature", 2)

    assert db.scan_by_prefix(3, "rec", "na") == ["nature(2)"]


def test_scan_all_fields_deleted():
    db = InMemoryDB()
    db.set(1, "rec", "f1", 10)
    db.delete(2, "rec", "f1")

    assert db.scan(3, "rec") == []
    assert db.scan_by_prefix(3, "rec", "f") == []
