from tasks import async_process_data


def async_process_data_event_handler(event: dict, context):
    unmatched_bonus = event.get("unmatched bonus", 6)
    mentees = event["mentees"]
    mentors = event["mentors"]
    return async_process_data(mentors, mentees, unmatched_bonus)
