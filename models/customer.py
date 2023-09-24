import sqlite3
from typing import Optional

conn = sqlite3.connect("data.sqlite3")
cursor = conn.cursor()


class Customer:
    def __init__(
            self,
            name: str,
            email: str,
            id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def create_table(cls):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS customers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   email TEXT
               )"""
        )
        conn.commit()

    @classmethod
    def create(cls, name: str, email: str) -> "Customer":
        cls.create_table()
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (?, ?)",
            (name, email),
        )
        conn.commit()
        return cls(name, email, cursor.lastrowid)

    @classmethod
    def get(cls, id_input: int) -> "Customer":
        cursor.execute("SELECT * FROM customers WHERE id = ?", str(id_input))
        result = cursor.fetchone()
        return cls(result[1], result[2], result[0])

    @classmethod
    def list(cls) -> list["Customer"]:
        cursor.execute("SELECT * FROM customers")
        result = cursor.fetchall()

        customers = []
        for row in result:
            customer = cls(id=row[0], name=row[1], email=row[2])
            customers.append(customer)
        return customers

    def update(self):
        cursor.execute(
            "UPDATE customers SET name=?, email=? WHERE id=?",
            (self.name, self.email, self.id),
        )
        conn.commit()

    def delete(self):
        cursor.execute("DELETE FROM customers WHERE id=?", (self.id,))
        conn.commit()
        self.id = None
