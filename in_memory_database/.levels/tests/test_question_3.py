from in_memory_database.solution import InMemoryDB


def test_set_with_ttl_exact_boundaries():
    db = InMemoryDB()
    db.set_with_ttl(100, "A", "x", 42, 50)

    # Válido no intervalo semi-aberto [100, 150)
    assert db.get(100, "A", "x") == 42
    assert db.get(125, "A", "x") == 42
    assert db.get(149, "A", "x") == 42
    assert db.get(150, "A", "x") is None
    assert db.get(151, "A", "x") is None


def test_ttl_with_scan_and_scan_by_prefix():
    db = InMemoryDB()
    db.set_with_ttl(100, "u", "f1", 10, 20)  # [100, 120)
    db.set(105, "u", "f2", 20)  # Permanente

    # Em t = 110, ambos existem
    assert db.scan(110, "u") == ["f1(10)", "f2(20)"]
    assert db.scan_by_prefix(110, "u", "f") == ["f1(10)", "f2(20)"]

    # Em t = 119, f1 ainda existe
    assert db.scan(119, "u") == ["f1(10)", "f2(20)"]

    # Em t = 120, f1 expirou exatamente
    assert db.scan(120, "u") == ["f2(20)"]
    assert db.scan_by_prefix(120, "u", "f") == ["f2(20)"]


def test_overwrite_ttl_with_permanent_set():
    db = InMemoryDB()
    db.set_with_ttl(10, "A", "k", 100, 10)  # Expiraria em 20
    db.set(15, "A", "k", 200)  # Sobrescreve como permanente

    assert db.get(25, "A", "k") == 200


def test_overwrite_permanent_with_ttl():
    db = InMemoryDB()
    db.set(10, "A", "k", 100)  # Permanente
    db.set_with_ttl(20, "A", "k", 200, 10)  # Vira temporário [20, 30)

    assert db.get(25, "A", "k") == 200
    assert db.get(30, "A", "k") is None


def test_overwrite_active_ttl_with_another_ttl():
    db = InMemoryDB()
    db.set_with_ttl(10, "A", "k", 100, 50)  # [10, 60)
    db.set_with_ttl(20, "A", "k", 200, 10)  # [20, 30)

    assert db.get(25, "A", "k") == 200
    assert db.get(30, "A", "k") is None
    assert db.get(59, "A", "k") is None


def test_delete_ttl_field_before_expiry():
    db = InMemoryDB()
    db.set_with_ttl(10, "A", "k", 100, 50)  # [10, 60)
    assert db.delete(20, "A", "k") is True
    assert db.get(25, "A", "k") is None
    # Deletar novamente retorna False
    assert db.delete(30, "A", "k") is False


def test_delete_expired_ttl_field_returns_false():
    db = InMemoryDB()
    db.set_with_ttl(10, "A", "k", 100, 10)  # [10, 20)

    assert db.delete(20, "A", "k") is False
    assert db.get(21, "A", "k") is None
