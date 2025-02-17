"""
mypy_menu.py

Handles the interactive menu for running and viewing MyPy results.
"""

from rich.console import Console
from rich.prompt import Prompt
from tool.mypy_formatter import format_summary, format_detailed_results
from tool.mypy_runner import run_mypy

console = Console()


def clear_screen():
    """Clears the console screen."""
    console.clear()


def run_mypy_menu(path: str):
    """
    Handles the interactive menu for MyPy analysis.

    Args:
        path (str): Path to analyze with MyPy.
    """
    while True:
        clear_screen()
        console.print(f"[bold green]Running MyPy on: {path}[/bold green]")

        # Run MyPy and get results
        results = run_mypy(path)

        # Check if no issues were found
        if not results or all(len(res.issues) == 0 for res in results):
            console.print(
                "[bold green]No issues detected! Type annotations are in good shape![/bold green]"
            )
            break

        # Display only the summary and overall score initially
        console.print("\n[bold cyan]MyPy Summary[/bold cyan]")
        file_mapping = format_summary(results, with_numbering=True)

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
            console.print("\n[bold cyan]MyPy Summary[/bold cyan]")
            format_summary(results, with_numbering=True)

        elif choice == "3":
            clear_screen()
            console.print("\n[bold cyan]MyPy Detailed Results[/bold cyan]")
            format_detailed_results(results)
            input("\nPress Enter to return to the menu...")

        elif choice == "4":
            continue  # Rerun the analysis

        elif choice == "5":
            console.print("[bold green]Exiting...[/bold green]")
            break
