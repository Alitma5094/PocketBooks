from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, DataTable, Label, Input
from models.invoice import Invoice
from models.invoice_item import InvoiceItem


class AddScreen(ModalScreen[tuple]):

    def compose(self) -> ComposeResult:
        yield Grid(
            # Label("Are you sure you want to quit?", id="question"),
            Input(placeholder="Description", id="description"),
            Button("Save", variant="success", id="save"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            description = self.query_one("#description", Input).value
            self.dismiss((description, 2, 123,))
        else:
            self.dismiss()


class InvoiceScreen(App):
    CSS_PATH = "invoice_screen.tcss"
    TITLE = "Invoice"

    def __init__(self, invoice: Invoice):
        super().__init__()
        self.invoice = invoice

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("n", "add_item", "Add Item"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Opened: " + self.invoice.date_opened.isoformat())
        yield Label("Due: " + self.invoice.date_due.isoformat())
        yield Label("Entries")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Description", "Qty", "Amount", "Subtotal")
        for item in InvoiceItem.list(self.invoice.id):
            table.add_row(item.description, item.qty, item.amount, "???")

    def action_add_item(self) -> None:
        def add_item(item: tuple) -> None:
            if item:
                new_item = InvoiceItem.create(self.invoice.id, item[0], item[1], item[2])
                table = self.query_one(DataTable)
                table.add_row(new_item.description, new_item.qty, new_item.amount, "???")

        self.push_screen(AddScreen(), add_item)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit(self) -> None:
        self.exit()
