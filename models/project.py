 #handles the projects of the individuals
from datetime import datetime

class Project:
    def __init__(self, title: str, description:str, due_date: str) :
        self.title = title
        self.description = description
        self.due_date = due_date

        self.tasks = [] # A list to hold task classes assigned to this project

    @property
    def due_date(self) -> str:
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: str):
        #Validates the dates in YYYY-MM-DD format
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self._due_date = value
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format (e.g., 2026-07-25).")

    def add_task(self, task_instance):
        #Appends a completed task instance to the project

        self.tasks.append(task_instance)
    
    def to_dict(self) -> dict:
        # converts object data to a dictionary for the json to save

        return{
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks] 
        }
        