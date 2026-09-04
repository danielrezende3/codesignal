from integer_container.solution import IntegerContainer


def test_median_of_empty_and_single_value_container():
    container = IntegerContainer()

    assert container.get_median() is None
    assert container.add(7) == 1
    assert container.get_median() == 7
    assert container.get_median() == 7


def test_median_with_odd_number_of_unsorted_values():
    container = IntegerContainer()
    for value in [9, 1, 7, 3, 5]:
        container.add(value)

    assert container.get_median() == 5


def test_even_median_is_the_lower_middle_value():
    container = IntegerContainer()
    for value in [40, 10, 30, 20]:
        container.add(value)

    assert container.get_median() == 20


def test_median_preserves_and_counts_duplicates():
    container = IntegerContainer()
    for value in [5, 3, 5, 5, 10, 3]:
        container.add(value)

    assert container.get_median() == 5
    assert container.add(3) == 7
    assert container.get_median() == 5
    assert container.add(3) == 8
    assert container.get_median() == 3


def test_median_updates_after_deletions():
    container = IntegerContainer()
    for value in [30, 20, 10]:
        container.add(value)

    assert container.get_median() == 20
    assert container.delete(30) is True
    assert container.get_median() == 10
    assert container.delete(10) is True
    assert container.get_median() == 20
    assert container.delete(20) is True
    assert container.get_median() is None


def test_median_with_negative_and_positive_values():
    container = IntegerContainer()
    for value in [-20, -10, 10, 20, 0]:
        container.add(value)

    assert container.get_median() == 0
    assert container.add(-30) == 6
    assert container.get_median() == -10
    assert container.add(30) == 7
    assert container.get_median() == 0
