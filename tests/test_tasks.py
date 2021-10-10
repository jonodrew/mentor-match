from app.tasks.tasks import process_data
from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.process import create_participant_list_from_path, process_data


def test_process_data(celery_app, celery_worker, known_file, test_data_path):
    known_file(test_data_path, "mentee", 50)
    known_file(test_data_path, "mentor", 50)
    mentees = create_participant_list_from_path(Mentee, test_data_path)
    mentors = create_participant_list_from_path(Mentor, test_data_path)
    mentors, mentees = process_data(mentors, mentees)
    assert mentees, mentors
