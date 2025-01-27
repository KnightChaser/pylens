"""
tool/pylint_formatter.py

Retrieves the results from pylint_runner.py and formats them for display,
using `rich` for better output formatting.
Currently, it shows the summary of the results and detailed results for each file.
"""

from typing import List, Dict
from rich.table import Table, box
from rich.console import Console
from tool.pylint_runner import PylintResult

console = Console()


def format_summary(
    results: List[PylintResult], overall_score: float, with_numbering: bool = False
) -> Dict[int, str]:
    """
    Formats and displays the summary of pylint results.

    Args:
        results (List[PylintResult]): List of pylint results.
        overall_score (float): The overall score from Pylint.
        with_numbering (bool): Whether to number files for selection.

    Returns:
        Dict[int, str]: Mapping of numbers to file names if with_numbering is True.
    """
    file_mapping = {}
    table = Table(
        title="Pylint Summary",
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
    )
    table.add_column("#" if with_numbering else "", justify="center", style="dim")
    table.add_column("File", style="dim", width=40)
    table.add_column("Total Issues", justify="center")
    table.add_column("Convention (C)", justify="center")
    table.add_column("Refactor (R)", justify="center")
    table.add_column("Warning (W)", justify="center")
    table.add_column("Error (E)", justify="center")
    table.add_column("Fatal (F)", justify="center")

    for idx, result in enumerate(results, start=1):
        counts = result.message_counts
        file_mapping[idx] = result.file
        table.add_row(
            str(idx) if with_numbering else "",
            result.file,
            str(len(result.issues)),
            str(counts["Convention"]),
            str(counts["Refactor"]),
            str(counts["Warning"]),
            str(counts["Error"]),
            str(counts["Fatal"]),
        )

    console.print(table)
    console.print(f"\n[bold green]Overall Score: {overall_score}/10[/bold green]")
    return file_mapping


def format_detailed_results(results: List[PylintResult]):
    """
    Formats and displays detailed pylint results.

    Args:
        results (List[PylintResult]): List of pylint results.
    """
    for result in results:
        console.print(f"\n[bold underline yellow]{result.file}[/bold underline yellow]")

        table = Table(show_header=True, header_style="bold cyan", box=box.MINIMAL)
        table.add_column("Line", style="dim", justify="right")
        table.add_column("Category", style="bold green", justify="center")
        table.add_column("Message", style="bold white")

        for issue in result.issues:
            table.add_row(
                str(issue.line),
                issue.category,
                issue.message,
            )

        console.print(table)
