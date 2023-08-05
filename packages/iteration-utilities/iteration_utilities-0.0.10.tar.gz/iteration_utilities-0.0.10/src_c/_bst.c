/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *
 * Would be very useful for "merge", this should be a reminder to include one.
 * Maybe based on "sortedcontainers"?
 *
 *****************************************************************************/


typedef struct {
    PyObject_HEAD
    PyObject *value;
    PyObject *left;
    PyObject *right;
} PyIUObject_BSTNode;

static PyTypeObject PyIUType_BSTNode;

/******************************************************************************
 *
 * New
 *
 *****************************************************************************/

static PyObject * bstnode_new(PyTypeObject *type, PyObject *args,
                              PyObject *kwargs) {
    PyIUObject_BSTNode *self;
    PyObject *item;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O:BSTNode", kwlist,
                                     &item)) {
        return NULL;
    }

    self = (PyIUObject_SortedList *)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    Py_INCREF(item);
    self->item = item;
    self->left = NULL;
    self->right = NULL;
    return (PyObject *)self;
}

/******************************************************************************
 *
 * New (only from C code)
 *
 * This bypasses the argument unpacking!
 *
 *****************************************************************************/

static PyIUObject_BSTNode * PyIU_BSTNode_FromC(PyObject *item) {
    // STEALS REFERENCES!!!
    PyIUObject_BSTNode *self;
    // Verify inputs
    if (item == NULL) {
        PyErr_Format(PyExc_TypeError, "`item` must be given.");
        return NULL;
    }
    self = PyObject_GC_New(PyIUObject_BSTNode, &PyIUType_BSTNode);
    if (self == NULL) {
        return NULL;
    }
    self->item = item;
    self->left = NULL;
    self->right = NULL;
    PyObject_GC_Track(self);
    return self;
}

/******************************************************************************
 *
 * Destructor
 *
 *****************************************************************************/

static void bstnode_dealloc(PyIUObject_ItemIdxKey *s) {
    Py_XDECREF(s->item);
    Py_XDECREF(s->left);
    Py_XDECREF(s->right);
    Py_TYPE(s)->tp_free((PyObject*)s);
}

/******************************************************************************
 *
 * Traverse
 *
 *****************************************************************************/

static int bstnode_traverse(PyIUObject_ItemIdxKey *s, visitproc visit,
                               void *arg) {
    Py_VISIT(s->item);
    Py_VISIT(s->left);
    Py_VISIT(s->right);
    return 0;
}

/******************************************************************************
 *
 * Representation
 *
 *****************************************************************************/

static PyObject * bstnode_repr(PyIUObject_ItemIdxKey *s) {
    return PyUnicode_FromFormat("BSTNode(item=%R)", s->item);
}

/******************************************************************************
 *
 * Docstring
 *
 *****************************************************************************/

PyDoc_STRVAR(bstnode_doc, "BSTNode(item)");


/******************************************************************************
 *
 * Type
 *
 *****************************************************************************/

static PyTypeObject PyIUType_BSTNode = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.BSTNode", /* tp_name */
    sizeof(PyIUObject_BSTNode), /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)bstnode_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    (reprfunc)bstnode_repr,    /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    bstnode_doc,               /* tp_doc */
    (traverseproc)bstnode_traverse, /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    bstnode_new,               /* tp_new */
    PyObject_GC_Del,           /* tp_free */
};
