# handles the tasks assigned to individuals

class Task:
    def __init__(self, title: str, assigned_to: str = "Unassigned",status: str = "Pending"):
        self.title = title

        self.assigned_to = assigned_to

        self._status = status #Protected attribute

    @property
    def status(self) -> str:
        return self._status
    
    def mark_complete(self):
        #updates the status to complete

        self._status = "Complete"

    def to_dict(self):
        # converts object data to a dictionary for the json to save

        return{
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }



       
