# a person class that handles attributes of individuals in the application

class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email # Protected attribute(Use of _)
    
    @property
    def email(self) -> str: #Getter for email
        return self._email

    @email.setter
    def email(self,value: str):
        # validates whether the email has an @ or .
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format.")
        
        self._email = value # for correct email format

    def __repr__(self) -> str: #Prints the name of the person using a cleaner format
        return(f"[{self.__class__.__name__}: {self.name}]")
        


        