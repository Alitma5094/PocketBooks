import typer
from subcommands import invoices, customers

app = typer.Typer()
app.add_typer(customers.app, name="customers", help="Manage customers")
app.add_typer(invoices.app, name="invoices", help="Manage invoices")

if __name__ == "__main__":
    app()
