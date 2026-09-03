from abc import ABC


class IntegerContainer(ABC):
    """
    `IntegerContainer` interface.
    """

    def add(self, value: int) -> int:
        """
        Should add the specified integer `value` to the container
        and return the number of integers in the container after the
        addition.
        """
        # default implementation
        return 0

    def delete(self, value: int) -> bool:
        """
        Should attempt to remove the specified integer `value` from
        the container.
        If the `value` is present in the container, remove it and
        return `True`, otherwise, return `False`.
        """
        # default implementation
        return False
