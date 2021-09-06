import pytest
from munkres import DISALLOWED, UnsolvableMatrix

from matching.helpers.pre_processing import check_unsolvability


def test_check_unsolvability():
    unsolvable_matrix = [
        [DISALLOWED, 161, DISALLOWED],
        [DISALLOWED, 1, DISALLOWED],
        [DISALLOWED, 157, DISALLOWED],
        [37, DISALLOWED, 5],
    ]
    with pytest.raises(UnsolvableMatrix):
        check_unsolvability(unsolvable_matrix)
