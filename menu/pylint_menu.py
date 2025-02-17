"""
pylint_menu.py

Handles the interactive menu for running and viewing Pylint results.
"""

from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from tool.pylint_formatter import format_summary, format_detailed_results
from tool.pylint_runner import run_pylint

console = Console()


def clear_screen():
    """Clears the console screen."""
    console.clear()


def run_pylint_menu(path: str, configuration: Optional[str] = None):
    """
    Handles the interactive menu for Pylint analysis.

    Args:
        path (str): Path to analyze with Pylint.
    """
    while True:
        clear_screen()
        console.print(f"[bold green]Running Pylint on: {path}[/bold green]")

        # Run pylint and get the results
        results, overall_score = run_pylint(paths=[path], configuration=configuration)

        # Check for no issues
        if not results:
            console.print(
                f"[bold green]No issues detected! Code quality looks perfect![/bold green]"
            )
            break

        # Display only the summary and overall score initially
        console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
        file_mapping = format_summary(results, overall_score, with_numbering=True)

        # Interactive menu
        console.print("\n[bold cyan]Options:[/bold cyan]")
        console.print(
            "[bold magenta]1.[/bold magenta] Show detailed results for a specific file"
        )
        console.print("[bold magenta]2.[/bold magenta] Show summary again")
        console.print("[bold magenta]3.[/bold magenta] Show all detailed results")
        console.print("[bold magenta]4.[/bold magenta] Rerun analysis")
        console.print("[bold magenta]5.[/bold magenta] Quit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
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
            clear_screen()
            console.print("\n[bold cyan]Pylint Summary[/bold cyan]")
            format_summary(results, overall_score, with_numbering=True)

        elif choice == "3":
            clear_screen()
            console.print("\n[bold cyan]Pylint Detailed Results[/bold cyan]")
            format_detailed_results(results)
            input("\nPress Enter to return to the menu...")

        elif choice == "4":
            continue  # Rerun the analysis

        elif choice == "5":
            console.print("[bold green]Exiting...[/bold green]")
            break
