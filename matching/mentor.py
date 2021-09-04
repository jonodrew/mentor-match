from matching.person import Person
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matching.mentee import Mentee


class Mentor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def mentees(self):
        return super().connections

    @mentees.setter
    def mentees(self, new_mentee: "Mentee"):
        super(Mentor, self).connections.append(new_mentee)
