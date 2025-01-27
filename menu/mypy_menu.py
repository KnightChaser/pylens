"""
mypy_menu.py

Handles the interactive menu for running and viewing Mypy results.
"""

from tool.mypy_runner import run_mypy


def run_mypy_menu(path: str):
    """
    Handles the interactive menu for Mypy analysis.

    Args:
        path (str): Path to analyze with Mypy.
    """
    results = run_mypy(path)

    from pprint import pprint

    pprint(results)
