from person import Person
from mentee import Mentee

class Mentor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mentees: list[Mentor] = []

    @property
    def mentors(self):
        return self._mentees

    @mentors.setter
    def mentors(self, new_mentee: Mentor):
        if len(self._mentees) < 3:
            self._mentees.append(new_mentee)
        else:
            raise Exception
