# Built-ins
from __future__ import absolute_import, division, print_function
import doctest


def doctest_module_no_failure(module):
    assert doctest.testmod(module).failed == 0
