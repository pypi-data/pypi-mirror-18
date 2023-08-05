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


ItemIdxKey = iteration_utilities.ItemIdxKey


@memory_leak_decorator()
def test_itemidxkey_getter():
    iik = ItemIdxKey(T(10), 2)
    assert iik.item == T(10)
    assert iik.idx == 2
    assert iik.key is None

    iik = ItemIdxKey(T(10), 2, T(5))
    assert iik.item == T(10)
    assert iik.idx == 2
    assert iik.key == T(5)


@memory_leak_decorator()
def test_itemidxkey_setter():
    iik = ItemIdxKey(T(10), 2)
    iik.item = T(20)
    assert iik.item == T(20)
    iik.idx = 10
    assert iik.idx == 10
    iik.key = T(0)
    assert iik.key == T(0)

    iik = ItemIdxKey(T(10), 2, T(5))
    iik.item = T(20)
    assert iik.item == T(20)
    iik.idx = 10
    assert iik.idx == 10
    iik.key = T(0)
    assert iik.key == T(0)


@memory_leak_decorator(collect=True)
def test_itemidxkey_setter_failure():
    iik = ItemIdxKey(T(10), 2)
    with pytest.raises(TypeError):
        iik.idx = 'a'

    iik = ItemIdxKey(T(10), 2, T(5))
    with pytest.raises(TypeError):
        iik.idx = 'a'


@memory_leak_decorator()
def test_itemidxkey_deleter():
    iik = ItemIdxKey(T(10), 2)
    del iik.key
    assert iik.key is None

    iik = ItemIdxKey(T(10), 2, T(5))
    del iik.key
    assert iik.key is None


@memory_leak_decorator(collect=True)
def test_itemidxkey_deleter_failure():
    iik = ItemIdxKey(T(10), 2)
    with pytest.raises(TypeError):
        del iik.item
    with pytest.raises(TypeError):
        del iik.idx

    iik = ItemIdxKey(T(10), 2, T(5))
    with pytest.raises(TypeError):
        del iik.item
    with pytest.raises(TypeError):
        del iik.idx


@memory_leak_decorator(offset=1)
def test_itemidxkey_pickle1():
    iik = ItemIdxKey(T(10), 2)
    x = pickle.dumps(iik)
    assert pickle.loads(x).item == T(10)
    assert pickle.loads(x).idx == 2


@memory_leak_decorator(offset=1)
def test_itemidxkey_pickle2():
    iik = ItemIdxKey(T(10), 2, T(5))
    x = pickle.dumps(iik)
    assert pickle.loads(x).item == T(10)
    assert pickle.loads(x).idx == 2
    assert pickle.loads(x).key == T(5)
