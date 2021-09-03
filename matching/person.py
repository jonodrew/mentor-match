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
        self.first_name: str = kwargs["Your first name"]
        self.last_name: str = kwargs["Your last name"]
        self.email_address: str = kwargs["Your Civil Service email address"]
        self.role: str = kwargs["Your job title or role"]
        self.department: str = kwargs["Your department or agency"]
        self._grade: int = GRADES.index(kwargs["Your grade"])
        self.profession: str = kwargs["Your profession"]

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, new_grade: str):
        if new_grade in GRADES:
            self._grade = GRADES.index(new_grade)
        else:
            raise NotImplementedError
