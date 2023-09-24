import typer
from typing_extensions import Annotated
from models.customer import Customer
from rich.prompt import Prompt

app = typer.Typer()


@app.command()
def create(
        name: Annotated[str, typer.Option(prompt=True, help="Customer's name")],
        email: Annotated[str, typer.Option(prompt=True, help="Customer's email")],
):
    """
    Create a new customer
    """
    new_cus = Customer.create(name=name, email=email)
    print(f"Created customer #{new_cus.id}")


@app.command("list")
def list_customers():
    """
   List customers
   """
    customers = Customer.list()
    for i in customers:
        print(f"{i.id}, {i.name}, {i.email}")


@app.command()
def update(id_input: Annotated[int, typer.Option("--id", prompt=True)]):
    """
   Update a customer
   """
    cus = Customer.get(id_input)
    cus.name = Prompt.ask("Name", default=cus.name)
    cus.email = Prompt.ask("Email", default=cus.email)
    cus.update()
    print(f"Updated customer #{cus.id}")


@app.command()
def delete(id_input: Annotated[int, typer.Option("--id", prompt=True, confirmation_prompt=True)]):
    """
   Delete a customer
   """
    cus = Customer.get(id_input)
    cus.delete()
    print(f"Deleted customer #{id_input}")
