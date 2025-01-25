"""
pylint_runner.py

It executes Pylint on the provided paths and parses the output.
The parsed output will be encapsulated in PylintResult and PylintIssue classes.
Those objects will be used by the output_formatter.py to display the results
in a more readable format using the rich library.
"""

import subprocess
from typing import List, Dict, Tuple
from pydantic import BaseModel


class PylintIssue(BaseModel):
    """
    Represents a single issue reported by Pylint.
    The association of this issue to which file will be done in the PylintResult class.
    In includes the following fields:
    - line: The line number where the issue was found.
    - category: The category of the issue (Convention, Refactor, Warning, Error, Fatal).
    - message: The message describing the issue.
    """

    line: int
    category: str
    message: str


class PylintResult(BaseModel):
    """
    Stores Pylint result for a single file.
    It includes the following fields:
    - file: The name of the file.
    - issues: A list of PylintIssue objects.
    - message_counts: A dictionary containing the count of issues for each category.
    """

    file: str
    issues: List[PylintIssue]
    message_counts: Dict[str, int]


CATEGORY_MAPPING = {
    "C": "Convention",
    "R": "Refactor",
    "W": "Warning",
    "E": "Error",
    "F": "Fatal",
}


def run_pylint(paths: List[str]) -> Tuple[List[PylintResult], float]:
    """
    Runs Pylint on the provided paths and parses the output.

    Args:
        paths (List[str]): List of paths to inspect.

    Returns:
        Tuple[List[PylintResult], float]: A list of Pylint results and the overall score.
    """
    results = []
    overall_score = None

    for path in paths:
        try:
            # Run pylint on the path
            result = subprocess.run(["pylint", path], capture_output=True, text=True)

            # Parse the output
            stdout_lines = result.stdout.splitlines()
            files_data = {}
            message_counts = {}
            current_file = None

            for line in stdout_lines:
                # Match overall score
                if "Your code has been rated at" in line:
                    overall_score = float(line.split("/")[0].split()[-1])

                # Match file headers
                if line.startswith("************* Module"):
                    current_file = line.split()[-1] + ".py"  # Add extension ".py"
                    files_data[current_file] = []
                    message_counts[current_file] = {
                        cat: 0 for cat in CATEGORY_MAPPING.values()
                    }

                # Match issue lines
                elif current_file and ":" in line:
                    parts = line.split(":", maxsplit=3)
                    if len(parts) == 4:
                        # Obtain the category name from the category letter by parsing each line
                        _, line_number, _, message = parts
                        code = message.split(":")[0].strip()[0]
                        category_letter = code.strip()[0]
                        category_name = CATEGORY_MAPPING.get(category_letter, "Unknown")

                        issue = PylintIssue(
                            line=int(line_number.strip()),
                            category=category_name,
                            message=message.strip(),
                        )
                        files_data[current_file].append(issue)
                        message_counts[current_file][category_name] += 1

            # Collect results
            for file, issues in files_data.items():
                results.append(
                    PylintResult(
                        file=file,
                        issues=sorted(
                            issues, key=lambda i: i.line
                        ),  # Sort issues(PylintIssue) by line number(PyLintIssue.line)
                        message_counts=message_counts[file],
                    )
                )

        except FileNotFoundError:
            print(
                "Error: Pylint is not installed. Please install it with 'pip install pylint'."
            )

    # Generally this can't happen, just to be sure and pass the pyright static anlaysis
    assert overall_score is not None, "Overall score must be calculated."

    return results, overall_score
