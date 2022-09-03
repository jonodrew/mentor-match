from collections import namedtuple
from copy import deepcopy

import functools
from matching.rules.rule import UnmatchedBonus
import matching.process as process

from classes import CSMentor, CSMentee, base_rules, CSPerson

Result = list[list[CSMentor], list[CSMentee], int]
ResultScore = namedtuple("ResultScore", ["count_mentors", "count_mentees"])


def async_process_data(
    mentors: list[CSMentor],
    mentees: list[CSMentee],
    unmatched_bonus: int = 6,
) -> Result:
    all_rules = [base_rules() for _ in range(3)]
    for ruleset in all_rules:
        ruleset.append(UnmatchedBonus(unmatched_bonus))
    matched_mentors, matched_mentees = process.process_data(
        mentors, mentees, all_rules=all_rules
    )
    return [matched_mentors, matched_mentees, unmatched_bonus]


def reduce_to_best_output(results: list[Result]) -> Result:
    return functools.reduce(compare_results, results)


def compare_results(first: Result, second: Result) -> Result:
    first_res = calculate_result_score(first)
    second_res = calculate_result_score(second)
    mapping = {first_res: first, second_res: second}
    if first_res.count_mentors == second_res.count_mentors:
        return mapping[max((first_res, second_res), key=lambda res: res.mentee_count)]
    else:
        return mapping[
            max((first_res, second_res), key=lambda result: result.count_mentors)
        ]


def calculate_result_score(result: Result) -> ResultScore:
    at_least_one_connection_fn = functools.partial(
        map, lambda participant: len(participant.connections) > 0
    )
    return ResultScore(
        count_mentees=sum(at_least_one_connection_fn(result[0])),
        count_mentors=sum(at_least_one_connection_fn(result[1])),
    )


def prepare_data_iterator(
    mentors: list[CSMentor], mentees: list[CSMentee]
) -> list[Result]:
    max_score = sum(rule.results.get(True) for rule in base_rules())
    return [[deepcopy(mentors), deepcopy(mentees), i] for i in range(max_score)]
