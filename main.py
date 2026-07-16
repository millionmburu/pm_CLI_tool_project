
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
        db["users"][new_user.email]= new_user.to_dict()
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
    
def create_project(db: dict):
    #Handles the creation of new projects
    console.print("\n[bold yellow]--- Create Project ---[/bold yellow]")
    title = input("Enter the project's title: ").strip()
    desc = input("Enter the project's description: ").strip()
    due_date = input("Enter the due date for the project(Format in YYYY-MM-DD): ").strip()

    #Incase the title for the project is left empty
    if not title:
        console.print("[bold red]Error: title cannot be empty![/bold red]")
        return
    
    #To deal with case insensitivity
    existing_titles_lower = {existing_title.lower() for existing_title in db["projects"]}
    #Incase the project already exists
    if title.lower() in existing_titles_lower:
        console.print("[bold red]Error: Project already exists![/bold red]")
        return
    try: 
        new_project = Project(title=title, description=desc, due_date=due_date)
        db["projects"][title] = new_project.to_dict()
        save_data(db)

        console.print(f"[bold green]Success: Created project '{title}'! Data saved to disk.[/bold green]")
    except ValueError as e:
        console.print(f"\n[bold red]Validation Error: {e}[/bold red]")    

def view_projects(db: dict):
    #Displays all the projects present in a table format
    console.print("\n[bold yellow]--- Project List ---[/bold yellow]")

    #Incase Project list is blank
    if not db["projects"]:
        console.print("[italic white]No Projects found. Create a new project[/italic white]")
        return
    
    for title, proj_data in db["projects"].items():
        #displays the project header
        project_header = f"[bold cyan]{title}[/bold cyan] | [italic]Due: {proj_data['due_date']}[/italic]\n[white]{proj_data['description']}[/white]"
        console.print(Panel(project_header, border_style="blue"))

        #renders tasks inside the project block 
        tasks = proj_data.get("tasks", [])
        if not tasks:
            console.print("  [dim italic white]No tasks added to this project yet.[/dim italic white]\n")
            continue
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Task Title", style="white")
        table.add_column("Assigned To", style="magenta")
        table.add_column("Status", style="bold green", justify="center")
        
        for task in tasks:
            status_color = "green" if task["status"] == "Complete" else "yellow"
            status_text = f"[{status_color}]{task['status']}[/{status_color}]"
            table.add_row(task["title"], task["assigned_to"], status_text)

        console.print(table)
        console.print("") #Line separator

def add_task_to_project(db: dict):
    #Adds a new task to existing projects
    console.print("\n[bold yellow]--- Add Task to Project ---[/bold yellow]")

    #Incase project is non_existant
    if not db["projects"]:
        console.print("[bold red]Error: No projects exist yet. Create a project first.[/bold red]")
        return

    input_project_title = input("Enter the project's name required to add the task to: ").strip()

    #Matching project with case insesnitivity
    project_title = None
    for actual_key in db["projects"]:
        if actual_key.lower() == input_project_title.lower():
            project_title = actual_key
            break
        
    #Incase the project title inputed is non_existant
    if not project_title:
        console.print("[bold red]Error: Project not found.[/bold red]")
        return
        
    task_title = input("Enter the task's name: ").strip()

    # Ensure task name is not empty
    if not task_title:
        console.print("[bold red]Error: Task name cannot be empty.[/bold red]")
        return

    # Check if a task with this name already exists in this project
    proj_data = db["projects"][project_title]
    existing_tasks = proj_data.get("tasks", [])
    existing_task_names_lower = {task["title"].lower() for task in existing_tasks}
    
    if task_title.lower() in existing_task_names_lower:
        console.print(f"[bold red]Error: A task named '{task_title}' already exists in this project.[/bold red]")
        return
    
    assigned_email = input("Enter the assigned's email address(press enter to leave it unassigned): ").strip()

    #Verifies whether the assigned exists in the database
    assignee_name = "Unassigned"

    if assigned_email:
        if assigned_email in db["users"]:
            assignee_name = db["users"][assigned_email]["name"]
        else:
            console.print("[bold red]Error: Assigned email matches no registered user. Setting task as Unassigned.[/bold red]")

    #Creates the task object
    new_task = Task(title=task_title, assigned_to=assignee_name)
        
    # Reconstruct project object, add task, and convert back to dictionary
    proj_data = db["projects"][project_title]
    try:
        project_obj = Project(proj_data["title"], proj_data["description"], proj_data["due_date"])
    except ValueError as e:
        console.print(f"[bold red]Database Error: The project '{project_title}' has an invalid due date format in storage. ({e})[/bold red]")
        return

    # Reload existing tasks as objects into our class
    for t_data in proj_data.get("tasks", []):
        project_obj.add_task(Task(t_data["title"], t_data["assigned_to"], t_data["status"]))

    #Appends the new task 
    project_obj.add_task(new_task)

    #Updates and saves the database
    db["projects"][project_title] = project_obj.to_dict()

    # Add project reference to user's project list if assigned
    if assigned_email and assigned_email in db["users"]:
        if project_title not in db["users"][assigned_email]["projects"]:
            db["users"][assigned_email]["projects"].append(project_title)

    save_data(db)
    console.print(f"[bold green]Success: Task '{task_title}' added to project '{project_title}'![/bold green]")

def mark_complete_tasks(db:dict):
    #Changes the status of tasks that are completed to "Complete" inside projects
    console.print("\n[bold yellow]--- Mark Task as Complete ---[/bold yellow]")
    input_project_title = input("Enter the project's title: ").strip()

    #Matching project with case insensitivity
    project_title = None
    for actual_key in db["projects"]:
        if actual_key.lower() == input_project_title.lower():
            project_title = actual_key
            break

    if not project_title:
        console.print("[bold red]Error: Project not found.[/bold red]")
        return

    task_title = input("Enter the exact task that has been completed: ").strip()

    if not task_title:
        console.print("[bold red]Error: Task name cannot be empty.[/bold red]")
        return
    
    proj_data = db["projects"][project_title]

    task_found = False

    #Looks through the data of tasks in the storage file
    for task_data in proj_data.get("tasks", []):
        if task_data["title"].lower() == task_title.lower():
            # Reconstruct the task, complete it, and save the updated status
            task_obj = Task(task_data["title"], task_data["assigned_to"], task_data["status"])
            task_obj.mark_complete()
            task_data["status"] = task_obj.status
            task_found = True
            break
    if task_found:
        save_data(db)
        console.print(f"[bold green]Success: Task '{task_title}' is now marked complete![/bold green]")
    else:
        console.print("[bold red]Error: Task not found in that project.[/bold red]")

def main():
    #The main application cycle
    """Main application loop."""
    # Load persistence database dictionary
    db = load_data()
    
    console.print("[bold green]Welcome to the Project Management CLI Tool![/bold green]")
    
    while True:
        display_menu()
        choice = input("Enter your command option (1-7): ").strip()
        
        if choice == "1":
            create_user(db)
        elif choice == "2":
            view_users(db)
        elif choice == "3":
            create_project(db)
        elif choice == "4":
            view_projects(db)
        elif choice == "5":
            add_task_to_project(db)
        elif choice == "6":
            mark_complete_tasks(db)
        elif choice == "7":
            console.print("[bold cyan]Goodbye! Have an productive day.[/bold cyan]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid option. Please enter a number between 1 and 7.[/bold red]")

if __name__ == "__main__":
    main()



