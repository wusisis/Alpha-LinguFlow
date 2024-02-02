from abc import ABC, abstractmethod

from resolver import pattern


@pattern(name="Int_Comparator")
class NumberComparator(ABC):
    """
    An abstract class for comparing integers.

    All classes inherited from this one should take an int and returns a bool.
    """

    def __init__(self): ...

    @abstractmethod
    def __call__(self, input: int) -> bool: ...


@pattern(name="Int_Greater_Or_Equal_Than")
class GreaterOrEqualThan(NumberComparator):
    """
    GreaterOrEqualThan checks if the input number is greater than or equal to the target value.
    """

    def __init__(self, value: int):
        self.value = value

    def __call__(self, input: int) -> bool:
        return input >= self.value


@pattern(name="Int_Less_Or_Equal_Than")
class LessOrEqualThan(NumberComparator):
    """
    LessOrEqualThan checks if the input number is less than or equal to the target value.
    """

    def __init__(self, value: int):
        self.value = value

    def __call__(self, input: int) -> bool:
        return input <= self.value


@pattern(name="Int_Greater_Than")
class GreaterThan(NumberComparator):
    """
    GreaterThan checks if the input number is greater than the target value.
    """

    def __init__(self, value: int):
        self.value = value

    def __call__(self, input: int) -> b