from time import sleep

import typer
from typing_extensions import Annotated
from models.invoice import Invoice
from models.invoice_item import InvoiceItem, cursor
from rich.console import Console
from rich.table import Table
from datetime import datetime
from tui_screens.invoice_screen import InvoiceScreen
from jinja2 import Environment, FileSystemLoader, select_autoescape
import tempfile

app = typer.Typer()


@app.command()
def create(
        customer: Annotated[int, typer.Option(prompt=True)],
        opened: Annotated[datetime, typer.Option(prompt=True)],
        due: Annotated[datetime, typer.Option(prompt=True)],
):
    new_invoice = Invoice.create(customer, opened, due)
    tui_app = InvoiceScreen(new_invoice)
    tui_app.run()


@app.command("list")
def list_invoices():
    invoices = Invoice.list()
    table = Table(title="Invoices")

    table.add_column("Id", justify="right", no_wrap=True)
    table.add_column("Date Opened")
    table.add_column("Customer")
    table.add_column("Amount", justify="right", no_wrap=True)

    for i in invoices:
        table.add_row(str(i.id), i.date_opened.isoformat(), "???", "$???")

    console = Console()
    console.print(table)


@app.command()
def delete(id_input: Annotated[int, typer.Option("--id", prompt=True, confirmation_prompt=True)]):
    invoice = Invoice.get(id_input)
    invoice.delete()
    print(f"Deleted invoice #{id}")


@app.command("print")
def print_invoice(id_input: Annotated[int, typer.Option("--id", prompt=True)]):
    invoice = Invoice.get(id_input)

    invoice_items = InvoiceItem.list(invoice.id)

    cursor.execute(
        "SELECT SUM(amount*qty) FROM invoice_items WHERE invoice_id = ?", (invoice.id,)
    )
    total_amount = cursor.fetchone()[0]

    env = Environment(
        loader=FileSystemLoader("templates/"), autoescape=select_autoescape()
    )
    template = env.get_template("invoice.html")

    with open("out.html", "w") as file:
        file.write(
            template.render(
                invoice_number=invoice.id,
                opened_date=invoice.date_opened,
                due_date=invoice.date_due,
                items=invoice_items,
                total_amount=total_amount,
            )
        )
    typer.launch("out.html")
    print("The invoice has been opened in your web browser. You can ether print it or save it as a PDF")

