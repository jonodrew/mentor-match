from matching.rules.rule import UnmatchedBonus
import matching.process as process

from classes import CSMentor, CSMentee, base_rules


def async_process_data(
    mentors,
    mentees,
    unmatched_bonus: int = 6,
) -> tuple[list[CSMentor], list[CSMentee], int]:
    all_rules = [base_rules() for _ in range(3)]
    for ruleset in all_rules:
        ruleset.append(UnmatchedBonus(unmatched_bonus))
    matched_mentors, matched_mentees = process.process_data(
        list(mentors), list(mentees), all_rules=all_rules
    )
    return matched_mentors, matched_mentees, unmatched_bonus
