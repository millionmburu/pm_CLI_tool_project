 #handles the projects of the individuals

class Project:
    def __init__(self, title: str, description:str, due_date: str) :
        self.title = title
        self.description = description
        self.due_date = due_date

        self.tasks = [] # A list to hold task classes assigned to this project

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
        