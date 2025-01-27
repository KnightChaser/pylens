"""
main.py

A CLI tool for running code quality tools like Pylint and displaying results.
"""

import typer
from rich.console import Console
from tool.pylint_formatter import format_summary, format_detailed_results
from tool.pylint_runner import run_pylint

app = typer.Typer()
console = Console()


@app.command()
def analyze(
    path: str = typer.Option(
        ..., "--path", "-p", help="Path to the directory or file to analyze."
    ),
    tool: str = typer.Option(
        "pylint", "--tool", "-t", help="The code quality tool to use (default: pylint)."
    ),
):
    """
    Analyze code using the specified tool and display the results.
    """
    if tool == "pylint":
        console.print(f"[bold green]Running Pylint on: {path}[/bold green]")

        # Run pylint and get the results
        results, overall_score = run_pylint([path])

        # Format and display the summary
        console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
        format_summary(results, overall_score)

        # Format and display detailed results
        console.print("\n[bold cyan]Pylint Detailed Results[/bold cyan]")
        format_detailed_results(results)

    else:
        console.print(
            f"[bold red]Error: Unsupported tool '{tool}'. Currently only 'pylint' is supported.[/bold red]"
        )


if __name__ == "__main__":
    app()
