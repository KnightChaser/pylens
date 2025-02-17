"""
main.py

A CLI tool for running code quality tools interactively with optional configuration files.
"""

import typer
from menu.pylint_menu import run_pylint_menu
from menu.mypy_menu import run_mypy_menu

app = typer.Typer()


@app.command()
def analyze(
    path: str = typer.Option(
        ..., "--path", "-p", help="Path to the directory or file to analyze."
    ),
    tool: str = typer.Option(
        "pylint", "--tool", "-t", help="The code quality tool to use (default: pylint)."
    ),
    configuration: str = typer.Option(
        None,
        "--configuration",
        "-c",
        help="Optional configuration file path for the tool (e.g., .pylintrc for Pylint, mypy.ini for MyPy).",
    ),
):
    """
    Analyze code using the specified tool and display results interactively.
    Allows optional configuration file for custom settings.
    """
    if tool == "pylint":
        run_pylint_menu(path=path, configuration=configuration)
    elif tool == "mypy":
        run_mypy_menu(path=path, configuration=configuration)
    else:
        typer.echo(
            f"Error: Unsupported tool '{tool}'. Currently supported tools are 'pylint' and 'mypy'."
        )


if __name__ == "__main__":
    app()
