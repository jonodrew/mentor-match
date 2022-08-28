from tasks import async_process_data


def async_process_data_event_handler(event: dict, context):
    unmatched_bonus = event.get("unmatched bonus", 6)
    mentees = event["mentees"]
    mentors = event["mentors"]
    matched_mentors, matched_mentees, bonus = async_process_data(
        mentors, mentees, unmatched_bonus
    )
    return {
        "mentors": [mentor.to_dict_for_output() for mentor in matched_mentors],
        "mentees": [mentee.to_dict_for_output() for mentee in matched_mentees],
        "unmatched bonus": bonus,
    }


def find_best_result_lambda(event: dict, context):
    return event
