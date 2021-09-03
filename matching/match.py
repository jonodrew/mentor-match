class Match:
    def __init__(self, mentor: "Mentor", mentee: "Mentee"):
        self.mentee = mentee
        self.mentor = mentor
        self.score: int = self.calculate_match()

    def calculate_match(self) -> int:
        return self._score_grade_match()

    def _score_grade_match(self) -> int:
        grade_diff = self.mentor.grade - self.mentee.grade
        if not (2 >= grade_diff > 0):
            return 0
        else:
            return grade_diff
