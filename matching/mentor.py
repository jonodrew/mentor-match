from matching.person import Person


class Mentor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mentees: list["Mentee"] = []

    @property
    def mentors(self):
        return self._mentees

    @mentors.setter
    def mentors(self, new_mentee: "Mentee"):
        if len(self._mentees) < 3:
            self._mentees.append(new_mentee)
        else:
            raise Exception
