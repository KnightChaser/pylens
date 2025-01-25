import os
import subprocess
from typing import List
from pydantic import BaseModel, field_validator


class PylintConfig(BaseModel):
    """
    Configuration for running Pylint on given paths.
    """

    paths: List[str]

    @field_validator("paths", mode="before")
    def validate_paths(cls, paths: List[str]) -> List[str]:
        """
        Validate that the list of paths is not empty and contains valid strings.
        """
        if not paths:
            raise ValueError("The list of paths cannot be empty.")
        for path in paths:
            if not isinstance(path, str) or not path.strip():
                raise ValueError(f"Invalid path: '{path}'")
            if not os.path.exists(path):
                raise ValueError(f"Path does not exist: '{path}'")
        return paths


def run_pylint(config: PylintConfig):
    """
    Run Pylint on the provided paths and print the results.

    Args:
        config (PylintConfig): Configuration containing the list of paths to inspect.
    """
    for path in config.paths:
        try:
            print(f"\nInspecting: {path}")
            result = subprocess.run(["pylint", path], capture_output=True, text=True)

            # Print the Pylint output
            print("Pylint Results:")
            print(result.stdout.strip())

            # Print any errors (if Pylint failed)
            if result.stderr:
                print("Pylint encountered an error:")
                print(result.stderr.strip())
        except FileNotFoundError:
            print(
                "Error: Pylint is not installed. Please install Pylint by running 'pip install pylint'."
            )


if __name__ == "__main__":
    # Define the paths to inspect
    paths_to_check = ["./testing"]

    # Validate and create the config
    try:
        pylint_config = PylintConfig(paths=paths_to_check)
        run_pylint(pylint_config)
    except ValueError as e:
        print(f"Configuration Error: {e}")
