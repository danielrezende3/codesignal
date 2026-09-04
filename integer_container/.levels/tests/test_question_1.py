from integer_container.solution import IntegerContainer


def test_add_returns_total_number_of_values():
    container = IntegerContainer()

    assert container.add(10) == 1
    assert container.add(100) == 2
    assert container.add(-5) == 3
    assert container.add(0) == 4


def test_duplicate_values_are_stored_individually():
    container = IntegerContainer()

    assert container.add(10) == 1
    assert container.add(10) == 2
    assert container.add(10) == 3

    assert container.delete(10) is True
    assert container.delete(10) is True
    assert container.delete(10) is True
    assert container.delete(10) is False


def test_delete_existing_and_missing_values():
    container = IntegerContainer()
    container.add(10)
    container.add(20)

    assert container.delete(30) is False
    assert container.delete(10) is True
    assert container.delete(10) is False
    assert container.delete(20) is True
    assert container.delete(20) is False


def test_delete_before_add_does_not_change_size():
    container = IntegerContainer()

    assert container.delete(5) is False
    assert container.add(5) == 1
    assert container.delete(5) is True
    assert container.add(7) == 1


def test_mixed_add_and_delete_operations():
    container = IntegerContainer()

    assert container.add(10) == 1
    assert container.add(15) == 2
    assert container.add(20) == 3
    assert container.add(10) == 4
    assert container.delete(15) is True
    assert container.delete(20) is True
    assert container.add(7) == 3
    assert container.delete(10) is True
    assert container.delete(10) is True
    assert container.delete(10) is False
    assert container.add(1) == 2
