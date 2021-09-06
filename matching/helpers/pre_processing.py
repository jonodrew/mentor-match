def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def check_unsolvability(matrix):
    """Checks additional conditions to see if an input Munkres cost matrix is unsolvable.

    Munkres v1.1.4 suffers from an infinite loop given some edge conditions, when it should,
    instead, emit a ``munkres.UnsolvableMatrix`` error. This function attempts to identify those
    conditions.

    Args:
        matrix (list): of lists of numbers, representing a cost matrix (or a profit matrix) suitable
            for Munkres optimization.

    Raises:
        munkres.UnsolvableMatrix: if the matrix is unsolvable.
    """

    from munkres import DISALLOWED
    from munkres import UnsolvableMatrix

    def _check_one_dimension_solvability():

        non_disallowed_indices = []  # (in possibly-offending rows)

        for row in matrix:

            # check to see if all but 1 cell in the row are DISALLOWED

            indices = [
                i for i, val in enumerate(row) if not isinstance(val, type(DISALLOWED))
            ]

            if len(indices) == 1:

                if indices[0] in non_disallowed_indices:
                    raise UnsolvableMatrix(
                        "Encountered edge condition that the Munkres library doesn't check for!"
                    )

                non_disallowed_indices.append(indices[0])

    _check_one_dimension_solvability()
    matrix = transpose_matrix(matrix)
    _check_one_dimension_solvability()
