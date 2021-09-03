GRADES = [
    "AA",
    "AO",
    "EO",
    "HEO",
    "SEO",
    "Grade 7",
    "Grade 6",
    "SCS1",
    "SCS2",
    "SCS3",
    "SCS4",
]


class Person:
    def __init__(self, **kwargs):
        self.first_name: str = kwargs["first name"]
        self.last_name: str = kwargs["last name"]
        self.email_address: str = kwargs["email address"]
        self.role: str = kwargs["role"]
        self.department: str = kwargs["department"]
        self._grade: int = GRADES.index(kwargs["grade"])
        self.profession: str = kwargs["profession"]

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, new_grade: str):
        if new_grade in GRADES:
            self._grade = GRADES.index(new_grade)
        else:
            raise NotImplementedError
