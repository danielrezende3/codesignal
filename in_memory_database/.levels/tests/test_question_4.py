from in_memory_database.solution import InMemoryDB


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


def test_get_at_ttl_exact_boundaries():
    db = InMemoryDB()
    db.set_with_ttl(10, "k", "v", 100, 10)  # [10, 20)

    assert db.get_at(100, "k", "v", 9) is None
    assert db.get_at(100, "k", "v", 10) == 100
    assert db.get_at(100, "k", "v", 19) == 100
    assert db.get_at(100, "k", "v", 20) is None


def test_get_at_overlapping_ttl_uses_latest_write():
    db = InMemoryDB()
    db.set_with_ttl(10, "k", "v", 100, 50)  # Substituído em t=20
    db.set_with_ttl(20, "k", "v", 200, 10)  # [20, 30)

    assert db.get_at(100, "k", "v", 19) == 100
    assert db.get_at(100, "k", "v", 20) == 200
    assert db.get_at(100, "k", "v", 29) == 200
    assert db.get_at(100, "k", "v", 30) is None
    assert db.get_at(100, "k", "v", 40) is None


def test_get_at_keeps_fields_and_records_isolated():
    db = InMemoryDB()
    db.set(10, "A", "x", 1)
    db.set(20, "A", "y", 2)
    db.set(30, "B", "x", 3)
    db.delete(40, "A", "x")

    assert db.get_at(100, "A", "x", 35) == 1
    assert db.get_at(100, "A", "x", 40) is None
    assert db.get_at(100, "A", "y", 50) == 2
    assert db.get_at(100, "B", "x", 50) == 3
