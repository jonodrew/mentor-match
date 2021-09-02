from person import Person
from mentor import Mentor

class Mentee(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mentors: list[Mentor] = []

    @property
    def mentors(self):
        return self._mentors

    @mentors.setter
    def mentors(self, new_mentor: Mentor):
        if len(self._mentors) < 3:
            self._mentors.append(new_mentor)
        else:
            raise Exception
