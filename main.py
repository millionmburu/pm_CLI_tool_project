
import sys

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage_handler import load_data, save_data

#Improves the terminal UI's look
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

#Initializes the console for styled printing
console = Console()

#makes the display panel of the terminal look better
def display_menu():
    menu_text = (
        "[bold cyan]1.[/bold cyan] Create a User\n"
        "[bold cyan]2.[/bold cyan] View Users\n"
        "[bold cyan]3.[/bold cyan] Create a Project\n"
        "[bold cyan]4.[/bold cyan] View Projects & Tasks\n"
        "[bold cyan]5.[/bold cyan] Add Task to Project\n"
        "[bold cyan]6.[/bold cyan] Mark Task as Complete\n"
        "[bold red]7. Exit[/bold red]"
    )
    console.print(Panel(menu_text, title="[bold green]PM CLI TOOL MENU[/bold green]", expand=False))

def create_user(db: dict):
    #Creates a new user with an email address with validation
    console.print("\n[bold yellow]--- Create New User ---[/bold yellow]")
    name = input("Enter your name: ").strip()
    email = input("Enter your email address: ").strip()

    #Incase either name or email address is left blank
    if not name or not email:
        console.print("[bold red]Error: Both name and email cannot be blank![/bold red]")
        return
    
    try:
        #creates a user instance that triggers the email validation function
        new_user = User(name=name, email=email)

        #saves to the database state
        db["user"][new_user.email]= new_user.to_dict()
        save_data(db)
        console.print(f"[bold green]Success: Created user '{new_user.name}'! Data saved to disk.[/bold green]")

    except ValueError as e:
        console.print(f"[bold red]Validation Error: {e}[/bold red]")

def view_users(db: dict):
    #enables to view users in a rich table
    console.print("\n[bold yellow]--- Registered Users ---[/bold yellow]")
    
    #Incase the users table is blank
    if not db["users"]:
        console.print("[italic white]No users found. Create a new user[/italic white]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="green")
    table.add_column("Assigned Projects Count", style="yellow", justify="center")

    for email, user_data in db["users"].items():
        project_count = str(len(user_data.get("projects", [])))
        table.add_row(user_data["name"], email, project_count)

    console.print(table)
    
