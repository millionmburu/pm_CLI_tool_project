
import pytest

from models.person import Person
from models.user import User
from models.task import Task
from models.project import Project

#~~~The User and Person Tests~~~

def test_user_inheretance_and_valid_email():
    #Verifies the User inherits from Person and validates the email
    
    user = User(name = "Million", email = "millionmureithimburu@gmail.com")
    assert user.name == "Million"
    assert user.email == "millionmureithimburu@gmail.com"
    assert isinstance(user, Person)

def test_user_invalid_email_raises_error():
    #Verifies whether an invalid email raises an error
    with pytest.raises(ValueError, match= "Invalid email format."):
        User(name= "Invalid user", email="million")


#~~~Project and Dates Test~~~

def test_project_creation_valid_date():
    #Verifies whether the project acccepts dates in YYYY-MM-DD format
    project = Project(
        title="Cash Register", 
        description="Python application", 
        due_date="2026-07-21"
    )
    assert project.title == "Cash Register"
    assert project.due_date == "2026-07-21"

def test_project_invalid_date_raises_error():
    #Verifies whether an invalid date raises an error for its format
    with pytest.raises(ValueError, match="Due date must be in YYYY-MM-DD format"):
        Project(title="Broken Project", description="Fail", due_date="19/7/2026")


#~~~Tasks and serialization Test~~~

def test_task_completion():
    #Verifies the task completion logic
    task = Task(title="Verify Logic", assigned_to="Million")
    assert task.status == "Pending"

    task.mark_complete()
    assert task.status == "Complete"

def test_project_to_dictionary_serialization():
    #Verifies whether exportation of projects to the dictionary is complete
    project = Project(
        title="Command Line Project", 
        description="A CLI Tool", 
        due_date="2026-07-19"
    )
    task = Task(title="Create the models", assigned_to="Million", status="Complete")
    project.add_task(task)

    data = project.to_dict()
    assert data["title"] == "Command Line Project"
    assert data["due_date"] == "2026-07-19"
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Create the models"


