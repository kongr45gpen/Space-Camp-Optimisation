from rich import print
from rich.panel import Panel
from pathlib import Path
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

import json

console = Console()

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")

card_db = {}
card_max_db = {}

# Read all files in directory ending in JSON sorted
for file in sorted(Path(".").glob("outputs/*.json")):
    js = file.read_text()
    content = json.loads(js)

    print(Panel("[b]Solution [blue]{}".format(file), expand=False))

    table = Table()

    for card, quant in content["variables"].items():
        if card not in card_db:
            card_db[card] = 0
        card_db[card] += quant

        if card not in card_max_db:
            card_max_db[card] = 0
        if quant > card_max_db[card]:
            card_max_db[card] = quant

    content["variables"] = {k: v for k, v in content["variables"].items() if v > 0}


    for card, quant in content["variables"].items():
        table.add_column(card[4:], justify="center", style="cyan", no_wrap=True)
    table.add_row(*[str(int(q)) for q in content["variables"].values()], style="magenta")

    total_cards = sum(content["variables"].values())

    console.print(table)

    for var, quant in content["intermediates"].items():
        if var in ["Score", "Cost"]:
            print("[bold]{}: [green]{:.0f}[/green][/bold]".format(var, quant), end="      ")
        elif var in ["xperience", "price", "efficiency"]:
            continue
        else:
            print("{}: {:.0f}".format(var, quant), end="    ")
    print("€/Score: [green]{:.2f}".format(content["intermediates"]["Cost"]/(content["intermediates"]["Score"]+1e-12)), end="      ")
    print("Cards: [yellow]{:.0f}".format(total_cards))
    print()
    print()
    print()

tables = []

# Print all cards sorted by popularity
print(Panel("[b]Card statistics", expand=False))
table = Table(title="Cards by popularity", title_justify="center", title_style="bold")
table.add_column("Card", justify="center", style="cyan", no_wrap=True)
table.add_column("Quantity", justify="center", style="magenta", no_wrap=True)
for card, quant in sorted(card_db.items(), key=lambda x: x[1], reverse=True):
    table.add_row(card[4:], str(int(quant)))
tables.append(table)

# Print the max quantity of each card
table = Table(title="Max cards", title_justify="center", title_style="bold")
table.add_column("Card", justify="center", style="cyan", no_wrap=True)
table.add_column("Quantity", justify="center", style="magenta", no_wrap=True)
for card, quant in sorted(card_max_db.items(), key=lambda x: x[1], reverse=True):
    table.add_row(card[4:], str(int(quant)))
tables.append(table)

console.print(Columns(tables, equal=False))