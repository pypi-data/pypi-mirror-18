# Built-ins
from __future__ import absolute_import, division, print_function
import pickle

# 3rd party
import pytest

# This module
import iteration_utilities

# Test helper
from helper_leak import memory_leak_decorator
from helper_cls import T, toT


nth = iteration_utilities.nth


@memory_leak_decorator()
def test_nth_normal1():
    assert nth(1)([T(1), T(2), T(3)]) == T(2)


@memory_leak_decorator()
def test_nth_normal2():
    assert nth(2)(map(T, range(10))) == T(2)


@memory_leak_decorator()
def test_nth_pred1():
    # With pred
    assert nth(1)([T(0), T(1), T(2)], pred=bool) == T(2)


@memory_leak_decorator()
def test_nth_pred2():
    assert nth(1)([T(0), T(1), T(2)], pred=None) == T(2)


@memory_leak_decorator()
def test_nth_pred3():
    assert nth(0)([T(0)]*100 + [T(1)], pred=bool) == T(1)


@memory_leak_decorator()
def test_nth_pred4():
    assert nth(1)([[T(0)], [T(1), T(2)]]*2,
                  pred=lambda x: len(x) > 1) == [T(1), T(2)]


@memory_leak_decorator()
def test_nth_predtruthyretpred1():
    # pred with truthy/retpred
    assert nth(1)([T(0), T(2), T(3), T(0)], pred=bool, truthy=False) == T(0)


@memory_leak_decorator()
def test_nth_predtruthyretpred2():
    assert not nth(1)([T(0), T(1), T(2), T(3), T(0)], pred=bool, truthy=False,
                      retpred=True)


@memory_leak_decorator()
def test_nth_predtruthyretpred3():
    assert nth(1)([T(0), T(2), T(3), T(0)], pred=lambda x: x**T(2),
                  truthy=False) == T(0)


@memory_leak_decorator()
def test_nth_predtruthyretpred4():
    assert nth(1)(toT([0, 1, 2, 3, 0]),
                  pred=lambda x: x**T(2), truthy=False, retpred=True) == T(0)


@memory_leak_decorator()
def test_nth_predtruthyretpred5():
    assert nth(2)([T(0), T(1), T(2), T(3)], pred=bool) == T(3)


@memory_leak_decorator()
def test_nth_predtruthyretpred6():
    assert nth(2)([T(0), T(1), T(2), T(3)], pred=bool, retpred=True)


@memory_leak_decorator()
def test_nth_predtruthyretpred7():
    assert nth(2)([T(0), T(1), T(2), T(3)], pred=lambda x: x**T(2)) == T(3)


@memory_leak_decorator()
def test_nth_predtruthyretpred8():
    assert nth(2)([T(0), T(2), T(3), T(4)], pred=lambda x: x**T(2),
                  retpred=True) == T(16)


@memory_leak_decorator()
def test_nth_default1():
    # With default
    assert nth(2)([], default=None) is None


@memory_leak_decorator()
def test_nth_default2():
    assert nth(1)([T(0), T(0), T(0)], default=None, pred=bool) is None


@memory_leak_decorator(collect=True)
def test_nth_failures1():
    # failures
    with pytest.raises(TypeError):
        nth(10)(T(100))


@memory_leak_decorator(collect=True)
def test_nth_failures2():
    with pytest.raises(IndexError):
        nth(10)([])


@memory_leak_decorator(collect=True)
def test_nth_failures3():
    with pytest.raises(IndexError):
        nth(1)([T(0)], pred=bool)


@memory_leak_decorator(collect=True)
def test_nth_failures4():
    with pytest.raises(TypeError):
        nth(1)([T('a'), T('b')], pred=lambda x: abs(x.value))


@memory_leak_decorator(collect=True)
def test_nth_failures5():
    with pytest.raises(TypeError):
        nth('a')


@memory_leak_decorator(offset=1)
def test_nth_pickle1():
    x = pickle.dumps(nth(2))
    assert pickle.loads(x)([T(1), T(2), T(3), T(4)]) == T(3)
