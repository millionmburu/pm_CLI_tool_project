#imports the person class from the person model

from models.person import Person 

class User(Person): #establishing an inheritance relationship
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

        self.projects = [] #holds the projects the person has 

    def to_dict(self) -> dict:
        # converts object data to a dictionary for the json to save

        return {
            "name": self.name,
            "email": self.email,
            "projects": self.projects
        }


