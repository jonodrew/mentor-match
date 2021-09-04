from typing import TYPE_CHECKING
from matching.person import Person

if TYPE_CHECKING:
    from matching.mentor import Mentor


class Mentee(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def mentors(self):
        return super(Mentee, self).connections

    @mentors.setter
    def mentors(self, new_mentor: "Mentor"):
        super(Mentee, self).connections.append(new_mentor)
