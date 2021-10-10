from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.person import GRADES


class ParticipantFactory:

    @classmethod
    def create_from_dict(cls, data_as_dict):
        if "mentor" in data_as_dict:
            participant_type = Mentor
        elif "mentee" in data_as_dict:
            participant_type = Mentee
        else:
            raise TypeError
        participant_data = data_as_dict[participant_type.__name__.lower()]
        participant = participant_type()
        participant._grade = GRADES.index(participant_data["grade"])
        participant.department = participant_data["department"]
        participant.profession = participant_data["profession"]
        participant.email = participant_data["email"]
        participant.first_name = participant_data["first name"]
        participant.last_name = participant_data["last name"]
        participant.role = participant_data["role"]
        connections = data_as_dict.get("connections", [])
        participant._connections = [ParticipantFactory.create_from_dict(connection_data) for connection_data in
                                    connections]
        return participant
