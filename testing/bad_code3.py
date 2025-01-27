# bad_code3.py
"""
This file is intentionally written with incorrect and inconsistent types
for testing the mypy type checker.
"""

def add_numbers(a: int, b: str) -> int:  # Incorrect type annotation
    return a + b  # Mixing int and str (logical error)


def greet_user(name: int) -> str:  # Name should be a string, but type is wrong
    return "Hello, " + name  # Concatenating str and int (type mismatch)


def get_item_length(item: list[int] | str) -> int:  # Accepts both list and str
    return len(item)  # len works, but no type check for elements in the list


def unsafe_casting(data: any) -> str:  # "any" used carelessly
    return data.upper()  # Assumes data is a string, but no check


def calculate_average(numbers: list) -> float:  # Missing type hint for list items
    return sum(numbers) / len(numbers)


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_age_in_dog_years(self) -> int:
        return self.age * "7"  # Multiplying int with str (logical error)


def main() -> None:
    add_numbers(5, "10")  # Should trigger mypy for incorrect type
    greet_user(1234)  # Passing int where str is expected
    print(get_item_length([1, 2, 3]))
    print(get_item_length("Hello"))
    print(unsafe_casting(123))  # Assumes 123 is a string, but will fail
    print(calculate_average(["1", "2", "3"]))  # Passing strings instead of numbers
    person = Person("Alice", "25")  # Age is given as str instead of int
    print(person.get_age_in_dog_years())


if __name__ == "__main__":
    main()

