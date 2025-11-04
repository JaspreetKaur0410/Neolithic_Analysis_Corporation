
from rich.table import Table
from rich.console import Console
console = Console()
def verdict_table(ticker: str, data: dict):
    table = Table(title=f"{ticker} — Neolithic v4.1 Verdict")
    table.add_column("Item"); table.add_column("Value")
    seen = set()
    for k, v in data.items():
        if k in seen: 
            continue
        seen.add(k)
        table.add_row(k, str(v))
    console.print(table); console.print()
