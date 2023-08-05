# Built-ins
from __future__ import absolute_import, division, print_function
import operator
import pickle

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
from helper_leak import memory_leak_decorator
from helper_cls import T


accumulate = iteration_utilities.accumulate


@memory_leak_decorator()
def test_accumulate_empty1():
    assert list(accumulate([])) == []


@memory_leak_decorator()
def test_accumulate_normal1():
    assert list(accumulate([T(1), T(2), T(3)])) == [T(1), T(3), T(6)]


@memory_leak_decorator()
def test_accumulate_normal2():
    assert list(accumulate([], None)) == []


@memory_leak_decorator()
def test_accumulate_normal3():
    assert list(accumulate([T(1), T(2), T(3), T(4)],
                           None)) == [T(1), T(3), T(6), T(10)]


@memory_leak_decorator()
def test_accumulate_binop1():
    assert list(accumulate([T(1), T(2), T(3), T(4)],
                           operator.add)) == [T(1), T(3), T(6), T(10)]


@memory_leak_decorator()
def test_accumulate_binop2():
    assert list(accumulate([T(1), T(2), T(3), T(4)],
                           operator.mul)) == [T(1), T(2), T(6), T(24)]


@memory_leak_decorator()
def test_accumulate_initial1():
    assert list(accumulate([T(1), T(2), T(3)],
                           None, T(10))) == [T(11), T(13), T(16)]


@memory_leak_decorator(collect=True)
def test_accumulate_failure1():
    with pytest.raises(TypeError):
        list(accumulate([T(1), T(2), T(3)], None, T('a')))


@memory_leak_decorator(collect=True)
def test_accumulate_failure2():
    with pytest.raises(TypeError):
        list(accumulate([T(1), T(2), T(3)], operator.add, T('a')))


@memory_leak_decorator(collect=True)
def test_accumulate_failure3():
    with pytest.raises(TypeError):
        list(accumulate([T('a'), T(2), T(3)]))


@pytest.mark.xfail(iteration_utilities.PY2, reason='pickle does not work on Python 2')
@memory_leak_decorator(offset=1)
def test_accumulate_pickle1():
    acc = accumulate([T(1), T(2), T(3), T(4)])
    assert next(acc) == T(1)
    x = pickle.dumps(acc)
    assert list(pickle.loads(x)) == [T(3), T(6), T(10)]


@pytest.mark.xfail(iteration_utilities.PY2, reason='pickle does not work on Python 2')
@memory_leak_decorator(offset=1)
def test_accumulate_pickle2():
    acc = accumulate([T(1), T(2), T(3), T(4)])
    x = pickle.dumps(acc)
    assert list(pickle.loads(x)) == [T(1), T(3), T(6), T(10)]


@pytest.mark.xfail(iteration_utilities.PY2, reason='pickle does not work on Python 2')
@memory_leak_decorator(offset=1)
def test_accumulate_pickle3():
    acc = accumulate([T(1), T(2), T(3), T(4)], operator.mul)
    assert next(acc) == T(1)
    x = pickle.dumps(acc)
    assert list(pickle.loads(x)) == [T(2), T(6), T(24)]


@pytest.mark.xfail(iteration_utilities.PY2, reason='pickle does not work on Python 2')
@memory_leak_decorator(offset=1)
def test_accumulate_pickle4():
    acc = accumulate([T(1), T(2), T(3), T(4)], None, T(4))
    x = pickle.dumps(acc)
    assert list(pickle.loads(x)) == [T(5), T(7), T(10), T(14)]
