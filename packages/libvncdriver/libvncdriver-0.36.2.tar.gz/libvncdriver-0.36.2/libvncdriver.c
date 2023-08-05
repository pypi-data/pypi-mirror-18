// libvncdriver.c - main file for libvncdriver module

#include <stdint.h>
#include <Python.h>

// Needed to access numpy array functionality from other C files
// http://docs.scipy.org/doc/numpy/reference/c-api.array.html#c.NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL libvncdriver_ARRAY_API
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/arrayobject.h"

#include "logger.h"
#include "vncsession.h"

// https://docs.python.org/3/howto/cporting.html
struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

#define ARRAY_SIZE(a) (sizeof(a)/sizeof((a)[0]))

// Module exception object
static PyObject *LibvncdriverError;

static PyObject *LibvncdriverMeraise(PyObject *self, PyObject *args) {
  PyErr_SetString(LibvncdriverError, "Raising test error");
  return NULL;
}

static PyObject *LibvncdriverSetup(PyObject *self, PyObject *args) {
  Py_INCREF(Py_None);
  return Py_None;
}

// Module methods
static PyMethodDef LibvncdriverMethods[] = {
  {"meraise", LibvncdriverMeraise, METH_NOARGS, "raise an exception"},
  {"setup", LibvncdriverSetup, METH_NOARGS,
      "Setup and initialize module internal state, required before use"},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "libvncdriver",
        NULL,
        sizeof(struct module_state),
        LibvncdriverMethods,
        NULL,
        NULL,  // traverse
        NULL,  // clear
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_libvncdriver(void)

#else
#define INITERROR return

void
initlibvncdriver(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("libvncdriver", LibvncdriverMethods);
#endif
  if (module == NULL)
    INITERROR;

  // Numpy C-API for arrays
  import_array();

  // Setup the logging class so we can use it
  if (logger_init() < 0)
    INITERROR;

  if (libvncdriver_init() < 0)
    INITERROR;

  // libvncdriver.VNCSession class
  if (PyType_Ready(&VNCSession_type) < 0) // Finalize type object
    INITERROR;  // Type initialization failed and set an exception, bail here
  Py_INCREF(&VNCSession_type);
  PyModule_AddObject(module, "VNCSession", (PyObject*)&VNCSession_type);

  // libvncdriver.Error exception
  LibvncdriverError = PyErr_NewException("libvncdriver.Error", NULL, NULL);
  Py_INCREF(LibvncdriverError);
  PyModule_AddObject(module, "Error", LibvncdriverError);

#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}
