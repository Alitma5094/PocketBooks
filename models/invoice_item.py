import sqlite3
from typing import Optional

conn = sqlite3.connect("data.sqlite3")
cursor = conn.cursor()


class InvoiceItem:
    def __init__(
            self,
            invoice_id: int,
            description: str,
            qty: int,
            amount: float,
            id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.invoice_id = invoice_id
        self.description = description
        self.qty = qty
        self.amount = amount

    @classmethod
    def create_table(cls):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS invoice_items (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   invoice_id INTEGER,
                   description TEXT,
                   qty INTEGER,
                   amount REAL
               )"""
        )
        conn.commit()

    @classmethod
    def create(cls, invoice_id: int, description: str, qty: int, amount: float) -> "InvoiceItem":
        cls.create_table()
        cursor.execute(
            "INSERT INTO invoice_items (invoice_id, description, qty, amount) VALUES (?, ?, ?, ?)",
            (invoice_id, description, qty, amount),
        )
        conn.commit()
        return cls(invoice_id, description, qty, amount, cursor.lastrowid)

    @classmethod
    def list(cls, invoice_id: int) -> list["InvoiceItem"]:
        cursor.execute(
            "SELECT * FROM invoice_items WHERE invoice_id=?", (invoice_id,)
        )
        result = cursor.fetchall()

        invoice_items = []
        for row in result:
            invoice_item = cls(
                invoice_id=row[1], description=row[2], qty=row[3], amount=row[4], id=row[0]
            )
            invoice_items.append(invoice_item)
        return invoice_items

    def update(self):
        if self.id is not None:
            cursor.execute(
                "UPDATE invoice_items SET invoice_id=?, description=?, qty=?, amount=? WHERE id=?",
                (self.invoice_id, self.description, self.qty, self.amount, self.id),
            )
            conn.commit()

    def delete(self):
        if self.id is not None:
            cursor.execute("DELETE FROM invoice_items WHERE id=?", (self.id,))
            conn.commit()
            self.id = None
