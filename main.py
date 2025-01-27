"""
main.py

A CLI tool for running code quality tools interactively.
"""

import typer
from menu.pylint_menu import run_pylint_menu

app = typer.Typer()


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
    Analyze code using the specified tool and display results interactively.
    """
    if tool == "pylint":
        run_pylint_menu(path)
    else:
        typer.echo(
            f"Error: Unsupported tool '{tool}'. Currently only 'pylint' is supported."
        )


if __name__ == "__main__":
    app()
