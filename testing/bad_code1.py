# This code is intentionally written poorly for testing Ruff and bad logic.

import os, sys  # Unused imports
import math  # Only partially used

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):  # Missing exception handling
        return math.pi * self.radius**2

    def circumference(self):  # Bad logic: allows negative radius
        return 2 * math.pi * self.radius

    def resize(self, factor):  # Misleading function: no validation of factor
        self.radius *= factor
        print(f"Radius is now {self.radius}")  # Prints even on invalid input


def process_circle(circle):  # No type hint or docstring
    try:
        print("Circle area:", circle.area())
        print("Circle circumference:", circle.circumference())
    except:  # Bare except, bad habit
        print("Something went wrong.")  # No error details provided


def main():
    bad_circle = Circle(-10)  # Poor practice: no check for negative radius
    bad_circle.resize("5")  # Bad logic: resizing with string instead of number
    process_circle(bad_circle)  # Function doesn't handle invalid circle correctly

if __name__ == "__main__":
    main()

