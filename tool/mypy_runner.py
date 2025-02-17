"""
tool/mypy_runner.py

Executes Mypy on the provided paths and parses the output into structured data.
"""

import os
import subprocess
from typing import List, Dict, Optional
from pydantic import BaseModel


class CodeLocation(BaseModel):
    """
    Represents a specific location in a file, with line and column numbers.
    For example, "15:4" would be CodeLocation(line=15, column=4).
    """

    line: int
    column: int


class MypyIssue(BaseModel):
    """
    Represents a single issue reported by Mypy.

    - filename: The name of the file.
    - issue_location_start: The starting location of the issue.
    - issue_location_end: The ending location of the issue.
    - category: The category of the issue (Error, Note).
    - message: The message describing the issue.
    - code_expression: The code expression associated with the issue.
    """

    filename: str
    issue_location_start: CodeLocation
    issue_location_end: CodeLocation
    category: str
    message: str
    code_expression: Optional[str] = None


class MypyResult(BaseModel):
    """
    Stores Mypy results for a single file.
    If there are n issues within a file, the class for that file will include n MypyIssue objects.

    - file: The name of the file.
    - issues: A list of MypyIssue objects.
    - message_counts: A dictionary containing the count of issues for each category(for statistics).
    """

    file: str
    issues: List[MypyIssue]
    message_counts: Dict[str, int]


CATEGORY_MAPPING = {
    "error": "Error",
    "note": "Note",
}


def parse_mypy_output(output: str) -> List[MypyResult]:
    """
    Parses the Mypy output into structured data.

    Args:
        output (str): The raw output from Mypy.

    Returns:
        List[MypyResult]: A list of structured Mypy results.
    """
    results: Dict[str, List[MypyIssue]] = {}
    message_counts: Dict[str, Dict[str, int]] = {}

    lines = output.splitlines()  # List of lines in the output
    current_file = None
    current_issue = None
    current_code_expression = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Detect file name and line-column range
        # It looks like: "file.py:line:col:line:col: category: message"
        if ":" in line and "error" in line or "note" in line:
            parts = line.split(":", maxsplit=4)
            if len(parts) >= 5:
                # Finalize the previous issue if there are pending code expressions
                if current_issue and current_code_expression:
                    current_issue.code_expression = "\n".join(current_code_expression)
                    current_code_expression.clear()

                # Parsing location and issue details
                current_file = parts[0]
                line_start, col_start = parts[1].strip(), parts[2].strip()
                line_end, col_end = parts[3].strip(), parts[4].split()[0].strip()
                col_end = col_end.strip(":")  # To remove the trailing colon
                category = parts[4].split()[1].strip(":")
                message = parts[4].split(":", maxsplit=1)[1].strip()

                # Create a new issue
                current_issue = MypyIssue(
                    filename=current_file,
                    issue_location_start=CodeLocation(
                        line=int(line_start), column=int(col_start)
                    ),
                    issue_location_end=CodeLocation(
                        line=int(line_end), column=int(col_end)
                    ),
                    category=CATEGORY_MAPPING.get(category, category),
                    message=message,
                )

                # Add the issue to the results
                # If the file is not in the results, add it with an empty list
                if current_file not in results:
                    results[current_file] = []
                    message_counts[current_file] = {
                        "Error": 0,
                        "Note": 0,
                        "Unknown": 0,
                    }
                results[current_file].append(current_issue)
                message_counts[current_file][
                    CATEGORY_MAPPING.get(category, "Unknown")
                ] += 1

        # Detect multiline code expressions (lines following an issue)
        elif current_issue:
            current_code_expression.append(line)
    # Finalize any remaining code expression
    if current_issue and current_code_expression:
        current_issue.code_expression = "\n".join(current_code_expression)

    # Convert results into a list of MypyResult objects
    return [
        MypyResult(file=file, issues=issues, message_counts=message_counts[file])
        for file, issues in results.items()
    ]


def run_mypy(path: str, configuration: Optional[str] = None) -> List[MypyResult]:
    """
    Executes Mypy on the given path and parses the output.

    Args:
        path (str): Path to analyze with Mypy.

    Returns:
        List[MypyResult]: A list of structured Mypy results.
    """
    try:
        # Check if configuration file is actually existing
        if configuration and not os.path.exists(configuration):
            raise FileNotFoundError(f"Configuration file not found: {configuration}")

        # Run Mypy command
        mypy_command = [
            "mypy",
            "--strict",
            "--pretty",
            "--show-error-context",
            "--show-column-numbers",
            "--show-error-codes",
            "--show-error-end",
            "--disallow-any-expr",
            "--disallow-any-decorated",
            "--disallow-any-explicit",
            "--disallow-any-generics",
            "--disallow-untyped-calls",
            "--disallow-untyped-defs",
            "--check-untyped-defs",
            "--warn-redundant-casts",
            "--warn-unused-ignores",
            "--warn-unreachable",
            "--ignore-missing-imports",
            path,
        ]

        if configuration:
            print(f"Using configuration file: {configuration}")
            mypy_command.append(f"--config-file={configuration}")

        result = subprocess.run(
            mypy_command,
            capture_output=True,
            text=True,
        )

        if result.returncode not in (
            0,  # Return code 0 indicates success
            1,  # Return code 1 indicates type-check errors
        ):  # Non-zero return code but not typical mypy errors
            print(f"Mypy execution failed:\n{result.stderr}")
            return []

        # Parse the output
        return parse_mypy_output(result.stdout)

    except FileNotFoundError:
        print(
            "Error: Mypy is not installed or provided configuration file does not exist."
        )
        return []
