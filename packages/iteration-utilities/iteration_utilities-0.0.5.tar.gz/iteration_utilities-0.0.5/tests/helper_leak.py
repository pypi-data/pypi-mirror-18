# Built-ins
from __future__ import absolute_import, division, print_function
from collections import Counter
from gc import get_objects, collect
from weakref import ref


def memory_leak(func, specific_object=None, exclude_object=ref):
    """Compares the number of tracked python objects before and after a
    function call and returns a dict containing differences.

    Parameters
    ----------
    func : callable
        The function that should be tested. Shouldn't return anything!

    specific_object : type, tuple of types, None, optional
        Test all tracked types (if it's ``None``) or only the specific type(s).
        Default is ``None``.

    exclude_object : type, tuple of types, None, optional
        Exclude specific type(s) or use all (if it's ``None``).
        Default is ``weakref.ref``.

    Returns
    -------
    difference : collections.Counter
        A Counter containing the types after the function call minus the ones
        before the function call. If the function doesn't return anything this
        Counter should be empty. If it contains types the function probably
        contains a memory leak.

    Notes
    -----
    It is convenient to wrap the explicit call inside a function that doesn't
    return. To enhance this useage the ``memory_leak`` function doesn't allow
    to pass arguments to the ``func``!
    """
    # Create Counter before listing the objects otherwise they would
    # be recognized as leak.
    before = Counter()
    after = Counter()

    # Tracked objects before the function call
    before.update(map(type, get_objects()))

    func()
    collect()

    # Tracked objects after the function call
    after.update(map(type, get_objects()))

    # Return the difference of all types the specified type.
    if specific_object is None:
        result = after - before
        if exclude_object is not None:
            if not isinstance(exclude_object, tuple):
                exclude_object = (exclude_object, )
            for exclude in exclude_object:
                if exclude in result:
                    del result[exclude]
        return result
    else:
        if not isinstance(specific_object, tuple):
            specific_object = (specific_object, )

        return Counter({specific: after[specific] - before[specific]
                        for specific in specific_object
                        if after[specific] - before[specific]})
