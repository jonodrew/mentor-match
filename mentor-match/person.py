from mentee import Mentee
from mentor import Mentor

GRADES = ["SCS4", "SCS3", "SCS2", "SCS1", "Grade 6", "Grade 7", "SEO", "HEO", "EO", "AO", "AA"].split(",")

class Person:

    def __init__(self, **kwargs):
        self.first_name: str = kwargs["first name"]
        self.last_name: str = kwargs["last name"]
        self.email_address: str = kwargs["email address"]
        self.role: str = kwargs["role"]
        self.department: str = kwargs["department"]
        self.grade: int = GRADES.index(kwargs["grade"])
        self.profession: str = kwargs["profession"]    
