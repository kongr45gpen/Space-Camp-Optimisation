from rich import print
from rich.panel import Panel
from pathlib import Path
from rich.table import Table
from rich.console import Console

import json

console = Console()

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")

# Read all files in directory ending in JSON sorted
for file in sorted(Path(".").glob("*.json")):
    js = file.read_text()
    content = json.loads(js)

    print(Panel("Solution [blue]{}".format(file)))

    table = Table(title="Cards used")

    content["variables"] = {k: v for k, v in content["variables"].items() if v > 0}

    for card, quant in content["variables"].items():
        table.add_column(card[4:], justify="center", style="cyan", no_wrap=True)
    table.add_row(*[str(int(q)) for q in content["variables"].values()], style="magenta")

    console.print(table)

    for var, quant in content["intermediates"].items():
        if var in ["Score", "Cost"]:
            print("[bold]{}: [green]{:.0f}[/green][/bold]".format(var, quant), end="      ")
        else:
            # Print without newline
            print("{}: {:.0f}".format(var, quant), end="    ")
    print()