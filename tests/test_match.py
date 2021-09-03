from matching.match import Match
from matching.mentor import Mentor
from matching.mentee import Mentee
from matching.person import GRADES
import pytest


@pytest.fixture
def base_data() -> dict:
    return {
        "first name": "Test",
        "last name": "Data",
        "email address": "test@data.com",
        "role": "N/A",
        "department": "Department of Fun",
        "grade": "Grade 7",
        "profession": "Policy",
    }


@pytest.fixture
def base_mentee(base_data):
    return Mentee(**base_data)


@pytest.fixture
def base_mentor(base_data):
    return Mentor(**base_data)


class TestMatch:
    def test_cant_match_with_same_department(
        self, base_mentee: Mentee, base_mentor: Mentor
    ):
        base_mentee.department = base_mentor.department = "Department of Fun"
        match = Match(base_mentor, base_mentee)
        assert match.score == 0

    @pytest.mark.parametrize("mentee_grade", [grade for grade in GRADES[0:-3]])
    @pytest.mark.parametrize("mentor_grade", [grade for grade in GRADES[3:]])
    def test_cant_match_with_greater_than_two_grade_difference(
        self, base_mentee, base_mentor, mentee_grade, mentor_grade
    ):
        base_mentee.grade = mentee_grade
        base_mentor.grade = mentor_grade

        match = Match(base_mentor, base_mentee)
        if GRADES.index(mentor_grade) - GRADES.index(mentee_grade) <= 2:
            pass
        else:
            assert match.score == 0
