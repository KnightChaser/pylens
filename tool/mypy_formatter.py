"""
mypy_formatter.py

Formats and displays MyPy results using `rich`, including summary and detailed results.
"""

from typing import List, Dict
from rich.table import Table
from rich.console import Console
from rich.text import Text
from tool.mypy_runner import MypyResult

console = Console()


def truncate_line(line: str, max_width: int) -> str:
    """
    Truncates a single line if it exceeds max_width, replacing excess with "...".
    """
    return line if len(line) <= max_width else line[: max_width - 3] + "..."


def format_code_expression(expression: str, max_width: int = 50) -> Text:
    """
    Processes multi-line code expressions, ensuring:
    - Each line is truncated if it exceeds max_width.
    - The entire block remains in a single table cell.

    Args:
        expression (str): The multi-line code snippet.
        max_width (int): Maximum width for each line.

    Returns:
        Text: A formatted Text object for `rich`.
    """
    lines = expression.split("\n")
    formatted_lines = [truncate_line(line, max_width) for line in lines]
    return Text("\n".join(formatted_lines), style="cyan")


def format_summary(
    results: List[MypyResult], with_numbering: bool = False
) -> Dict[int, str]:
    """
    Formats and displays the summary of MyPy results.

    Args:
        results (List[MypyResult]): List of MyPy results.
        with_numbering (bool): If True, adds numbering for files to reference in menus.

    Returns:
        Dict[int, str]: A mapping of file index to file names for menu selection.
    """
    table = Table(title="MyPy Summary", show_header=True, header_style="bold magenta")
    table.add_column(
        "#" if with_numbering else "", justify="right", style="bold magenta"
    )
    table.add_column("File", style="dim", width=40)
    table.add_column("Total Issues", justify="center")
    table.add_column("Errors", justify="center")
    table.add_column("Notes", justify="center")

    file_mapping = {}
    for idx, result in enumerate(results, start=1):
        counts = result.message_counts
        if with_numbering:
            file_mapping[idx] = result.file

        table.add_row(
            str(idx) if with_numbering else "N/A",
            result.file,
            str(len(result.issues)),
            str(counts["Error"]),
            str(counts["Note"]),
        )

    console.print(table)
    return file_mapping


def format_detailed_results(results: List[MypyResult]):
    """
    Formats and displays detailed MyPy results.

    Args:
        results (List[MypyResult]): List of MyPy results.
    """
    for result in results:
        console.print(f"\n[bold underline yellow]{result.file}[/bold underline yellow]")

        table = Table(
            show_header=True, header_style="bold cyan", show_lines=True
        )  # Show row separators
        table.add_column("Line", style="dim", justify="right")
        table.add_column("Column", style="dim", justify="right")
        table.add_column("Category", style="bold green", justify="center")
        table.add_column("Message", style="bold white")
        table.add_column(
            "Code Expression", style="italic white", width=50, justify="left"
        )

        for issue in result.issues:
            formatted_expression = (
                format_code_expression(issue.code_expression, max_width=50)
                if issue.code_expression
                else ""
            )

            table.add_row(
                str(issue.issue_location_start.line),
                str(issue.issue_location_start.column),
                issue.category,
                issue.message,
                formatted_expression if formatted_expression else "N/A",
            )

        console.print(table)
