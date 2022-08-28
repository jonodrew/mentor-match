from copy import deepcopy

from tasks import async_process_data
from classes import base_rules


def async_process_data_event_handler(event: dict, context):
    """
    Event handler that calls the `tasks.async_process_data` function.
    :param event: A dictionary with an event from AWS. Must have the "mentees" and "mentors" keys
    :param context: The AWS context
    :return:
    """
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
    """
    Event handler to find the "best" unmatched bonus value. See `tasks.find_best_output` for implementation details
    :param event: The triggering event. An array that should consist of
    {"mentor": [...], "mentee": [...], "unmatched bonus": int} dicts
    :param context: The AWS context
    :return: A single {"mentor": [...], "mentee": [...], "unmatched bonus": int} dict
    """
    return event


def prepare_data_for_mapping(event: dict, context) -> list[dict]:
    """
    Create fresh copies of data, ready for handing to the mapping State defined in the infrastructure
    :param event: The data to be matched
    :param context: The AWS context
    :return: A list of dicts with the format {"mentor": [...], "mentee": [...], "unmatched bonus": int}
    """
    max_score = sum(rule.results.get(True) for rule in base_rules())
    mentees = event["mentees"]
    mentors = event["mentors"]
    copies = ((deepcopy(mentors), deepcopy(mentees), i) for i in range(max_score))
    return [
        {"unmatched bonus": copy[2], "mentors": copy[0], "mentees": copy[1]}
        for copy in copies
    ]
