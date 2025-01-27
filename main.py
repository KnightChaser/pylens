"""
main.py

A CLI tool for running code quality tools like Pylint and displaying results interactively.
"""

import typer
from rich.console import Console
from rich.prompt import Prompt
from tool.pylint_formatter import format_summary, format_detailed_results
from tool.pylint_runner import run_pylint

app = typer.Typer()
console = Console()


def clear_screen():
    """Clears the console screen."""
    console.clear()


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
    Analyze code using the specified tool and display the results interactively.
    """
    if tool == "pylint":
        while True:
            clear_screen()
            console.print(f"[bold green]Running Pylint on: {path}[/bold green]")

            # Run pylint and get the results
            results, overall_score = run_pylint([path])

            # Check for no issues
            if not results:
                console.print(
                    f"[bold green]No issues detected! Code quality looks perfect![/bold green]"
                )
                break

            # Display only the summary and overall score initially
            console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
            file_mapping = format_summary(results, overall_score, with_numbering=True)

            # Interactive menu (option)
            console.print("\n[bold cyan]Options:[/bold cyan]")
            console.print(
                "[bold magenta]1.[/bold magenta] Show detailed results for a specific file"
            )
            console.print("[bold magenta]2.[/bold magenta] Show summary again")
            console.print("[bold magenta]3.[/bold magenta] Show all detailed results")
            console.print("[bold magenta]4.[/bold magenta] Rerun analysis")
            console.print("[bold magenta]5.[/bold magenta] Quit")

            choice = Prompt.ask(
                "\nEnter your choice", choices=["1", "2", "3", "4", "5"]
            )

            if choice == "1":
                # "Show detailed results for a specific file"
                file_choice = Prompt.ask(
                    "Enter the number of the file to see details",
                    choices=[str(i) for i in file_mapping.keys()],
                )
                clear_screen()
                selected_file = file_mapping[int(file_choice)]
                detailed_result = [res for res in results if res.file == selected_file]
                if detailed_result:
                    console.print(
                        f"\n[bold cyan]Detailed Results for {selected_file}[/bold cyan]"
                    )
                    format_detailed_results(detailed_result)
                input("\nPress Enter to return to the menu...")

            elif choice == "2":
                # "Show summary again"
                clear_screen()
                console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
                format_summary(results, overall_score, with_numbering=True)

            elif choice == "3":
                # "Show all detailed results"
                clear_screen()
                console.print("\n[bold cyan]Pylint Detailed Results[/bold cyan]")
                format_detailed_results(results)
                input("\nPress Enter to return to the menu...")

            elif choice == "4":
                # Rerun the analysis
                continue

            elif choice == "5":
                # "Exit"
                console.print("[bold green]Exiting...[/bold green]")
                break

    else:
        console.print(
            f"[bold red]Error: Unsupported tool '{tool}'. Currently only 'pylint' is supported.[/bold red]"
        )


if __name__ == "__main__":
    app()
