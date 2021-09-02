from person import Person
from mentee import Mentee
from mentor import Mentor

class Match:
    def __init__(self, mentor: Mentor, mentee: Mentee):
        self.mentee = mentee
        self.mentor = mentor
        self.score: int = self.calculate_match()

    def calculate_match(self) -> int:
        return 0
