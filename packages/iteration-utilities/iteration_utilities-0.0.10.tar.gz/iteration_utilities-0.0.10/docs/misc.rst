Miscellanea
-----------

`iteration_utilities` implements some general utilities that were useful in
some of the implementations. Some of these might even be useful in other
contexts, so these are summarized here.

- :py:func:`~iteration_utilities.ItemIdxKey`, a class to facilitate stable
  sorting supporting `reverse` and `key`.
- :py:func:`~iteration_utilities.Seen`, a class that wraps a `set` and a `list`
  supporting ``in`` operations and a ``contains_add`` method to facilitate
  keeping track of already seen objects (even if they are unhashable).
