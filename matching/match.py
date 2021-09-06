import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matching.mentor import Mentor
    from matching.mentee import Mentee


class Match:
    def __init__(self, mentor: "Mentor", mentee: "Mentee", weightings=None):
        self.weightings = (
            {"profession": 4, "grade": 3, "unmatched bonus": 0}
            if weightings is None
            else weightings
        )
        self.mentee = mentee
        self.mentor = mentor
        self._disallowed: bool = False
        self._score: int = 0
        self.calculate_match()

    @property
    def score(self):
        if self._disallowed:
            return 0
        else:
            return self._score

    @score.setter
    def score(self, new_value: int):
        self._score += new_value

    @property
    def disallowed(self):
        return self._disallowed

    @disallowed.setter
    def disallowed(self, new_value: bool):
        if self._disallowed is False and new_value is True:
            self._disallowed = new_value

    def calculate_match(self) -> None:
        scoring_methods = [
            self.check_not_already_matched,
            self.score_department,
            self.score_grade,
            self.score_profession,
            self.score_unmatched,
        ]
        while not self._disallowed and scoring_methods:
            scoring_method = scoring_methods.pop()
            scoring_method()

    def score_grade(self) -> None:
        grade_diff = self.mentor.grade - self.mentee.grade
        if not (2 >= grade_diff > 0):
            self._disallowed = True
        else:
            self._score += grade_diff * self.weightings["grade"]

    def score_profession(self) -> None:
        if self.mentee.profession == self.mentor.profession:
            self._score += self.weightings["profession"]

    def score_department(self) -> None:
        if self.mentee.department == self.mentor.department:
            self._disallowed = True

    def score_unmatched(self) -> None:
        if any(
            map(
                lambda participant: len(participant.connections) == 0,
                (self.mentee, self.mentor),
            )
        ):
            self._score += self.weightings.get("unmatched bonus")

    def mark_successful(self):
        if not self.disallowed:
            self.mentor.mentees.append(self.mentee)
            self.mentee.mentors.append(self.mentor)
        else:
            logging.debug("Skipping this match as disallowed")

    def check_not_already_matched(self):
        if self.mentee in self.mentor.mentees or self.mentor in self.mentee.mentors:
            self._disallowed = True
