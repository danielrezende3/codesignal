from mock3.solution import InMemoryDB


def test_set_get_and_delete_basic():
    db = InMemoryDB()
    db.set(1, "user1", "age", 26)
    db.set(2, "user1", "score", 100)

    assert db.get(3, "user1", "age") == 26
    assert db.get(4, "user1", "score") == 100
    assert db.get(5, "user1", "missing_field") is None
    assert db.get(6, "missing_user", "age") is None

    assert db.delete(7, "user1", "age") is True
    assert db.get(8, "user1", "age") is None
    assert db.delete(9, "user1", "age") is False


def test_overwrite_field_and_values():
    db = InMemoryDB()
    db.set(1, "A", "val", 10)
    assert db.get(2, "A", "val") == 10
    db.set(3, "A", "val", 20)
    assert db.get(4, "A", "val") == 20
    db.set(
        5, "A", "val", 0
    )  # Value 0 should be stored and returned as 0, not treated as None/falsy
    assert db.get(6, "A", "val") == 0


def test_multiple_keys_isolation():
    db = InMemoryDB()
    db.set(1, "user1", "email", 1)
    db.set(2, "user2", "email", 2)
    assert db.get(3, "user1", "email") == 1
    assert db.get(4, "user2", "email") == 2

    assert db.delete(5, "user1", "email") is True
    assert db.get(6, "user1", "email") is None
    assert db.get(7, "user2", "email") == 2  # user2 untouched
