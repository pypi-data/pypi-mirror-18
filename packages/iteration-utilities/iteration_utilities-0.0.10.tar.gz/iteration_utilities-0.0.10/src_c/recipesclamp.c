/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    PyObject *iterator;
    PyObject *low;
    PyObject *high;
    int inclusive;
} PyIUObject_Clamp;

static PyTypeObject PyIUType_Clamp;

/******************************************************************************
 *
 * New
 *
 *****************************************************************************/

static PyObject * clamp_new(PyTypeObject *type, PyObject *args,
                            PyObject *kwargs) {
    static char *kwlist[] = {"iterable", "low", "high", "inclusive", NULL};
    PyIUObject_Clamp *lz;

    PyObject *iterable, *iterator, *low=NULL, *high=NULL;
    int inclusive = 0;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOi:clamp", kwlist,
                                     &iterable, &low, &high, &inclusive)) {
        return NULL;
    }

    /* Create and fill struct */
    iterator = PyObject_GetIter(iterable);
    if (iterator == NULL) {
        return NULL;
    }
    lz = (PyIUObject_Clamp *)type->tp_alloc(type, 0);
    if (lz == NULL) {
        Py_DECREF(iterator);
        return NULL;
    }
    Py_XINCREF(low);
    Py_XINCREF(high);
    lz->iterator = iterator;
    lz->low = low;
    lz->high = high;
    lz->inclusive = inclusive;
    return (PyObject *)lz;
}

/******************************************************************************
 *
 * Destructor
 *
 *****************************************************************************/

static void clamp_dealloc(PyIUObject_Clamp *lz) {
    PyObject_GC_UnTrack(lz);
    Py_XDECREF(lz->iterator);
    Py_XDECREF(lz->low);
    Py_XDECREF(lz->high);
    Py_TYPE(lz)->tp_free(lz);
}

/******************************************************************************
 *
 * Traverse
 *
 *****************************************************************************/

static int clamp_traverse(PyIUObject_Clamp *lz, visitproc visit, void *arg) {
    Py_VISIT(lz->iterator);
    Py_VISIT(lz->low);
    Py_VISIT(lz->high);
    return 0;
}

/******************************************************************************
 *
 * Next
 *
 *****************************************************************************/

static PyObject * clamp_next(PyIUObject_Clamp *lz) {

    PyObject *item;
    int res;

    while ( (item = (*Py_TYPE(lz->iterator)->tp_iternext)(lz->iterator)) ) {
        // Check if it's smaller than the lower bound
        if (lz->low != NULL) {
            res = PyObject_RichCompareBool(item, lz->low,
                                           lz->inclusive ? Py_LE : Py_LT);
            if (res == 1) {
                Py_DECREF(item);
                continue;
            } else if (res == -1) {
                Py_DECREF(item);
                return NULL;
            }
        }
        // Check if it's bigger than the upper bound
        if (lz->high != NULL) {
            res = PyObject_RichCompareBool(item, lz->high,
                                           lz->inclusive ? Py_GE : Py_GT);
            if (res == 1) {
                Py_DECREF(item);
                continue;
            } else if (res == -1) {
                Py_DECREF(item);
                return NULL;
            }
        }
        // Still here? Return the item!
        return item;
    }
    PYIU_CLEAR_STOPITERATION;
    return NULL;
}

/******************************************************************************
 *
 * Reduce
 *
 *****************************************************************************/

static PyObject * clamp_reduce(PyIUObject_Clamp *lz) {
    if (lz->low == NULL && lz->high == NULL) {
        return Py_BuildValue("O(O)(i)", Py_TYPE(lz),
                             lz->iterator, lz->inclusive);
    } else if (lz->high == NULL) {
        return Py_BuildValue("O(OO)(i)", Py_TYPE(lz),
                             lz->iterator, lz->low, lz->inclusive);
    } else if (lz->low == NULL) {
        return Py_BuildValue("O(O)(Oi)", Py_TYPE(lz),
                             lz->iterator, lz->high, lz->inclusive);
    } else {
        return Py_BuildValue("O(OOOi)", Py_TYPE(lz),
                             lz->iterator, lz->low, lz->high, lz->inclusive);
    }
}

/******************************************************************************
 *
 * Setstate
 *
 *****************************************************************************/

static PyObject * clamp_setstate(PyIUObject_Clamp *lz, PyObject *state) {
    PyObject *high=NULL;
    int inclusive;

    if (PyTuple_Size(state) == 2) {
        if (!PyArg_ParseTuple(state, "Oi", &high, &inclusive)) {
            return NULL;
        }
    } else {
        if (!PyArg_ParseTuple(state, "i", &inclusive)) {
            return NULL;
        }
    }
    if (high != NULL) {
        Py_CLEAR(lz->high);
        Py_XINCREF(high);
        lz->high = high;
    }
    lz->inclusive = inclusive;
    Py_RETURN_NONE;
}

/******************************************************************************
 *
 * Methods
 *
 *****************************************************************************/

static PyMethodDef clamp_methods[] = {
    {"__reduce__", (PyCFunction)clamp_reduce, METH_NOARGS, PYIU_reduce_doc},
    {"__setstate__", (PyCFunction)clamp_setstate, METH_O, PYIU_setstate_doc},
    {NULL, NULL}
};

/******************************************************************************
 *
 * Docstring
 *
 *****************************************************************************/

PyDoc_STRVAR(clamp_doc, "clamp(iterable, [low, high, inclusive])\n\
\n\
Remove values which are not between `low` and `high`.\n\
\n\
Parameters\n\
----------\n\
iterable : iterable\n\
    Clamp the values from this `iterable`.\n\
\n\
low : any type, optional\n\
    The lower bound for clamp.\n\
\n\
high : any type, optional\n\
    The upper bound for clamp.\n\
\n\
inclusive : bool, optional\n\
    If ``True`` also remove values that are equal to `low` and `high`.\n\
    Default is ``False``.\n\
\n\
Returns\n\
-------\n\
clamped : generator\n\
    A generator containing the values of `iterable` which are between `low`\n\
    and `high`.\n\
\n\
Examples\n\
--------\n\
This function is equivalent to a generator expression like:\n\
``(item for item in iterable if low <= item <= high)`` or\n\
``(item for item in iterable if low < item < high)`` if `inclusive=True`.\n\
Or a similar `filter`: ``filter(lambda item: low <= item <= high, iterable)``\n\
But it also allows for either ``low`` or ``high`` to be ignored and is faster.\n\
Some simple examples::\n\
\n\
    >>> from iteration_utilities import clamp\n\
    >>> list(clamp(range(5), low=2))\n\
    [2, 3, 4]\n\
    >>> list(clamp(range(5), high=2))\n\
    [0, 1, 2]\n\
    >>> list(clamp(range(1000), low=2, high=8, inclusive=True))\n\
    [3, 4, 5, 6, 7]");

/******************************************************************************
 *
 * Type
 *
 *****************************************************************************/

static PyTypeObject PyIUType_Clamp = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.clamp",        /* tp_name */
    sizeof(PyIUObject_Clamp),           /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)clamp_dealloc,          /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_reserved */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    PyObject_GenericGetAttr,            /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,            /* tp_flags */
    clamp_doc,                          /* tp_doc */
    (traverseproc)clamp_traverse,       /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    PyObject_SelfIter,                  /* tp_iter */
    (iternextfunc)clamp_next,           /* tp_iternext */
    clamp_methods,                      /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    PyType_GenericAlloc,                /* tp_alloc */
    clamp_new,                          /* tp_new */
    PyObject_GC_Del,                    /* tp_free */
};
