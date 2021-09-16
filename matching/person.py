from typing import List

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
        self._grade: int = GRADES.index(kwargs["Your grade"])
        self.department: str = kwargs["Your department or agency"]
        self.profession: str = kwargs["Your profession"]
        self.data: dict = kwargs
        self._connections: List[Person] = []
        self.has_no_match: bool = False

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, new_grade: str):
        if new_grade in GRADES:
            self._grade = GRADES.index(new_grade)
        else:
            raise NotImplementedError

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, new_connection: "Person"):
        if len(self._connections) < 3:
            self._connections.append(new_connection)
        else:
            raise Exception

    def to_dict(self, depth=1) -> dict:
        output = {
            "email": self.data.get("Your Civil Service email address"),
            "first name": self.data.get("Your first name"),
            "last name": self.data.get("Your last name"),
            "role": self.data.get("Your job title or role"),
            "department": self.department,
            "grade": GRADES[self.grade],
            "profession": self.profession,
        }
        if depth == 1:
            for i, connection in enumerate(self.connections):
                for key, value in connection.to_dict(depth=0).items():
                    output[f"match {i+1} {key}"] = value
        return output
