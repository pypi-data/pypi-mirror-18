# Built-ins
from __future__ import absolute_import, division, print_function
from itertools import tee

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
from helper_doctest import doctest_module_no_failure


def test_doctests():
    doctest_module_no_failure(iteration_utilities._recipes._core)
    doctest_module_no_failure(iteration_utilities._recipes._additional)
    doctest_module_no_failure(iteration_utilities._helpers._performance)


def test_exceptions():
    # old-style classes don't have the subclasses special member.
    if iteration_utilities.PY2:
        class A:
            pass
        with pytest.raises(TypeError):
            list(iteration_utilities.itersubclasses(A))

    # Random product doesn't work with empty iterables
    with pytest.raises(IndexError):
        iteration_utilities.random_product([])

    # There is no element 10 in the tee object so this will raise the
    # Exception.
    t1, t2 = tee([1, 2, 3, 4, 5])
    with pytest.raises(IndexError):
        iteration_utilities.tee_lookahead(t1, 10)

    # Missing idx or start/stop in replace/remove/getitem
    with pytest.raises(TypeError):
        iteration_utilities.replace([1, 2, 3], 5)
    with pytest.raises(TypeError):
        iteration_utilities.remove([1, 2, 3])
    with pytest.raises(TypeError):
        iteration_utilities.getitem([1, 2, 3])
    # Stop smaller than start in replace/remove
    with pytest.raises(ValueError):
        iteration_utilities.replace(range(10), 5, start=7, stop=5)
    with pytest.raises(ValueError):
        iteration_utilities.remove(range(10), start=7, stop=5)
    # idx smaller than -1 in getitem
    with pytest.raises(ValueError):
        iteration_utilities.getitem(range(10), (4, 2, -3, 9))


def test_empty_input():
    empty = []

    assert iteration_utilities.all_isinstance(empty, float)

    assert not iteration_utilities.any_isinstance(empty, float)

    assert iteration_utilities.consume(empty, 2) is None

    assert list(iteration_utilities.deepflatten(empty)) == []

    assert iteration_utilities.dotproduct(empty, empty) == 0

    assert list(iteration_utilities.flatten(empty)) == []

    assert list(iteration_utilities.getitem(
        range(10), empty)) == []

    x, y = iteration_utilities.ipartition(empty, lambda x: x)
    assert list(x) == [] and list(y) == []

    # no need to test iter_subclasses here

    assert list(iteration_utilities.ncycles(empty, 10)) == []

    assert list(iteration_utilities.powerset(empty)) == [()]

    assert iteration_utilities.random_combination(empty, 0) == ()
    assert iteration_utilities.random_combination(empty, 0, True) == ()

    assert iteration_utilities.random_permutation(empty, 0) == ()

    assert list(iteration_utilities.remove(
        range(10), empty)) == list(range(10))

    assert list(iteration_utilities.replace(
        range(10), 20, empty)) == list(range(10))

    # no need to test repeatfunc here

    # no need to test tabulate here

    assert list(iteration_utilities.tail(empty, 2)) == []

    # no need to test tee_lookahead here
