from matching.match import Match
from matching.mentor import Mentor
from matching.mentee import Mentee
from matching.person import GRADES
import pytest


class TestMatch:
    def test_cant_match_with_same_department(
        self, base_mentee: Mentee, base_mentor: Mentor
    ):
        base_mentee.department = base_mentor.department = "Department of Fun"
        match = Match(base_mentor, base_mentee)
        match.calculate_match()
        assert match.disallowed

    @pytest.mark.parametrize("mentee_grade", [grade for grade in GRADES])
    @pytest.mark.parametrize("mentor_grade", [grade for grade in GRADES])
    def test_cant_match_with_greater_than_two_grade_difference(
        self, base_mentee, base_mentor, mentee_grade, mentor_grade
    ):
        base_mentee.grade = mentee_grade
        base_mentor.grade = mentor_grade

        match = Match(base_mentor, base_mentee)
        match.calculate_match()
        if GRADES.index(mentor_grade) - GRADES.index(mentee_grade) <= 2:
            pass
        else:
            assert match.disallowed

    def test_matching_profession_scores_four_points(self, base_mentor, base_mentee):
        base_mentor.grade = "Grade 6"  # 1 grade diff
        base_mentor.department = "Department of Sad"
        match = Match(base_mentor, base_mentee)
        assert match.score - match.weightings["grade"] == 4

    def test_mark_successful(self, base_mentee, base_mentor):
        match = Match(base_mentor, base_mentee)
        match.mark_successful()
        assert base_mentor in base_mentee.mentors
        assert base_mentee in base_mentor.mentees

    def test_cant_match_with_self(self, base_mentee, base_data):
        mentor = Mentor(**base_data)
        match = Match(mentor, base_mentee)
        match.calculate_match()
        assert match.disallowed

    def test_cant_match_with_someone_already_matched_with(
        self, base_mentee, base_mentor
    ):
        base_mentor.mentees.append(base_mentee)
        test_match = Match(base_mentor, base_mentee)
        test_match.calculate_match()
        assert test_match.disallowed
