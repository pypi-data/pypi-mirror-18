# Built-ins
from __future__ import absolute_import, division, print_function
import pickle

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
from helper_leak import memory_leak_decorator
from helper_cls import T


one = iteration_utilities.one


@memory_leak_decorator()
def test_one_normal1():
    assert one([T(0)]) == T(0)


@memory_leak_decorator()
def test_one_normal2():
    assert one('a') == 'a'


@memory_leak_decorator()
def test_one_normal3():
    assert one({T('o'): T(10)}) == T('o')


@memory_leak_decorator(collect=True)
def test_one_failure1():
    with pytest.raises(TypeError):
        one(T(0))


@memory_leak_decorator(collect=True)
def test_one_failure2():
    # empty iterable
    with pytest.raises(ValueError):
        one([])


@memory_leak_decorator(collect=True)
def test_one_failure3():
    # more than 1 element
    with pytest.raises(ValueError):
        one([T(1), T(2)])
