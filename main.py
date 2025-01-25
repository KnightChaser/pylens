"""
main.py

A main script that runs Pylint on the provided paths and displays the results.
"""

from pylint_runner import run_pylint
from output_formatter import format_summary, format_detailed_results
from rich.console import Console

console = Console()

if __name__ == "__main__":
    # Paths to inspect
    # TODO: Such options should be configurable. Let's employ an environment file(.env) later
    paths_to_check = ["./testing"]

    # Run pylint and get the results
    results, overall_score = run_pylint(paths_to_check)

    # Format and display the summary
    console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
    format_summary(results, overall_score)

    # Format and display detailed results
    console.print("\n[bold cyan]Pylint Detailed Results[/bold cyan]")
    format_detailed_results(results)
