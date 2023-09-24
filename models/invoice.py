import sqlite3
from datetime import datetime
from typing import Optional

conn = sqlite3.connect("data.sqlite3")
cursor = conn.cursor()


class Invoice:
    def __init__(
            self,
            customer_id: int,
            date_opened: datetime,
            date_due: datetime,
            id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.customer_id = customer_id
        self.date_opened = date_opened
        self.date_due = date_due

    @classmethod
    def create_table(cls):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS invoices (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_id INTEGER,
                   date_opened TEXT,
                   date_due TEXT
               )"""
        )
        conn.commit()

    @classmethod
    def create(cls, customer_id: int, date_opened: datetime, date_due: datetime) -> "Invoice":
        cls.create_table()
        cursor.execute(
            "INSERT INTO invoices (customer_id, date_opened, date_due) VALUES (?, ?, ?)",
            (customer_id, date_opened, date_due),
        )
        conn.commit()
        return cls(customer_id, date_opened, date_due, cursor.lastrowid)

    @classmethod
    def list(cls) -> list["Invoice"]:
        cursor.execute("SELECT * FROM invoices")
        result = cursor.fetchall()

        invoices = []
        for row in result:
            invoice = cls(
                customer_id=row[1], date_opened=datetime.fromisoformat(row[2]), date_due=datetime.fromisoformat(row[3]),
                id=row[0]
            )
            invoices.append(invoice)
        return invoices

    def update(self):
        if self.id is not None:
            cursor.execute(
                "UPDATE invoices SET customer_id=?, date_opened=?, date_due=? WHERE id=?",
                (self.customer_id, self.date_opened, self.date_due, self.id),
            )
            conn.commit()

    @classmethod
    def get(cls, id_input: int) -> "Invoice":
        cursor.execute("SELECT * FROM invoices WHERE id = ?", str(id_input))
        result = cursor.fetchone()
        return cls(
            customer_id=result[1], date_opened=datetime.fromisoformat(result[2]),
            date_due=datetime.fromisoformat(result[3]), id=result[0]
        )

    def delete(self):
        if self.id is not None:
            cursor.execute("DELETE FROM invoices WHERE id=?", (self.id,))
            conn.commit()
            self.id = None
