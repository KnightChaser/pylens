# This code is intentionally written poorly for testing Ruff and bad logic.

from random import choice  # Unused import
import json  # Unused import

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        for item in self.data:
            print(f"Processing item: {item}")  # Potentially prints sensitive info
        # Missing logic to validate items or handle processing failures


def write_to_file(filename, content):  # Missing exception handling
    file = open(filename, "w")  # Bad practice: missing `with` context manager
    file.write(content)
    file.close()


def nested_logic_example():  # Poorly structured function
    data = [1, 2, 3, "a", None]
    total = 0
    for item in data:
        try:
            if isinstance(item, int):  # Redundant check, mixed logic
                total += item
            elif item == "a":
                raise ValueError("Invalid data: 'a'")
        except ValueError as e:
            print(f"Error: {e}")
        finally:
            print("Finished processing item.")  # Misleading message


def main():
    processor = DataProcessor([1, "2", None])  # Poor practice: no data validation
    processor.process()

    write_to_file("output.txt", "{'key': value}")  # Invalid JSON written to file

    nested_logic_example()

if __name__ == "__main__":
    main()

