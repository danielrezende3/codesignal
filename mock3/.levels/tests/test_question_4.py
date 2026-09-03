from mock3.solution import InMemoryDB


def test_get_at_historical_queries_basic():
    db = InMemoryDB()
    db.set(10, "A", "x", 100)
    db.set_with_ttl(20, "A", "x", 200, 20)  # [20, 40)
    db.set(50, "A", "x", 300)

    assert db.get_at(100, "A", "x", 15) == 100
    assert db.get_at(101, "A", "x", 25) == 200
    assert db.get_at(102, "A", "x", 45) is None
    assert db.get_at(103, "A", "x", 60) == 300


def test_get_at_before_creation_and_nonexistent():
    db = InMemoryDB()
    db.set(20, "user", "score", 50)

    # Antes da criação inicial
    assert db.get_at(100, "user", "score", 10) is None
    assert db.get_at(100, "user", "score", 19) is None
    # No exato momento da criação
    assert db.get_at(100, "user", "score", 20) == 50
    # Registro ou campo inexistente
    assert db.get_at(100, "missing", "score", 50) is None
    assert db.get_at(100, "user", "missing", 50) is None


def test_get_at_with_delete_and_recreation():
    db = InMemoryDB()
    db.set(10, "key", "f", 100)  # [10, 30) -> 100
    db.delete(30, "key", "f")  # [30, 50) -> None
    db.set(50, "key", "f", 200)  # [50, 70) -> 200
    db.delete(70, "key", "f")  # >= 70    -> None

    assert db.get_at(100, "key", "f", 10) == 100
    assert db.get_at(100, "key", "f", 29) == 100
    assert db.get_at(100, "key", "f", 30) is None
    assert db.get_at(100, "key", "f", 49) is None
    assert db.get_at(100, "key", "f", 50) == 200
    assert db.get_at(100, "key", "f", 69) == 200
    assert db.get_at(100, "key", "f", 70) is None
    assert db.get_at(100, "key", "f", 100) is None


def test_get_at_multiple_ttls_and_overrides():
    db = InMemoryDB()
    db.set_with_ttl(10, "k", "v", 10, 10)  # [10, 20) -> 10
    db.set_with_ttl(30, "k", "v", 20, 10)  # [30, 40) -> 20
    db.set(40, "k", "v", 30)  # >= 40    -> 30

    assert db.get_at(100, "k", "v", 15) == 10
    assert db.get_at(100, "k", "v", 25) is None
    assert db.get_at(100, "k", "v", 35) == 20
    assert db.get_at(100, "k", "v", 40) == 30
    assert db.get_at(100, "k", "v", 99) == 30
