# Built-ins
from __future__ import absolute_import, division, print_function

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
from helper_leak import memory_leak_decorator
from helper_cls import T, toT


partition = iteration_utilities.partition


@memory_leak_decorator()
def test_partition_empty1():
    assert partition([]) == (toT([]), toT([]))


@memory_leak_decorator()
def test_partition_normal1():
    assert partition([T(0), T(1), T(2)]) == (toT([0]), toT([1, 2]))


@memory_leak_decorator()
def test_partition_normal2():
    assert partition([T(3), T(1), T(0)]) == (toT([0]), toT([3, 1]))


@memory_leak_decorator()
def test_partition_normal3():
    assert partition([T(0), T(0), T(0)]) == (toT([0, 0, 0]), [])


@memory_leak_decorator()
def test_partition_normal4():
    assert partition([T(1), T(1), T(1)]) == ([], toT([1, 1, 1]))


@memory_leak_decorator()
def test_partition_pred1():
    assert partition([T(0), T(1), T(2)],
                     lambda x: x.value > 1) == (toT([0, 1]), toT([2]))


@memory_leak_decorator()
def test_partition_pred2():
    assert partition([T(0), T(1), T(2)],
                     lambda x: x.value < 1) == (toT([1, 2]), toT([0]))


@memory_leak_decorator(collect=True)
def test_partition_failure1():
    # not-iterable
    with pytest.raises(TypeError):
        partition(T(10))


@memory_leak_decorator(collect=True)
def test_partition_failure2():
    with pytest.raises(TypeError):
        partition([T(1), T('a')], lambda x: x.value + 3)


@memory_leak_decorator(collect=True)
def test_partition_failure3():

    with pytest.raises(TypeError):
        partition([T(1), T('a')], lambda x: x.value - 1)


@memory_leak_decorator(collect=True)
def test_partition_failure4():
    with pytest.raises(TypeError):
        partition([T(1), T('a')], lambda x: x.value + 'a')
