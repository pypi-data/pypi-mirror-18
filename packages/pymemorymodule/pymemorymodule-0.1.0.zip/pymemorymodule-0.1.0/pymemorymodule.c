#include <Python.h>
#include <Windows.h>
#include "MemoryModule.h"

static PyObject *c_void_p = NULL;

/*
 * Magic for Python 2.6 or below
 * http://py3c.readthedocs.io/en/latest/capsulethunk.html
 */
#if PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION < 7
    #define PyCapsule_New(pointer, name, destructor) \
        (PyCObject_FromVoidPtr(pointer, (void (*)(void*)) (destructor)))
    #define PyCapsule_GetPointer(capsule, name) \
        (PyCObject_AsVoidPtr(capsule))
#endif

/*
 * Difference of R/O binary data between Python 2.x and Python 3.x
 */
#if PY_MAJOR_VERSION >= 3
    #define READONLY_BUFFER "y#"
#else
    #define READONLY_BUFFER "t#"
#endif

/*
 * Port MemoryModule's functions
 * https://github.com/fancycode/MemoryModule/blob/master/MemoryModule.h
 * https://github.com/fancycode/MemoryModule/blob/master/MemoryModule.c
 */
#define DOCSTRING_MemoryLoadLibrary "MemoryLoadLibrary(data):\n" \
    "\n" \
    "Load EXE/DLL from given data.\n" \
    "\n" \
    "All dependencies are resolved using default LoadLibrary\n" \
    "and GetProcAddress calls through the Windows API.\n" \
    "\n" \
    "  :param data: Data of EXE/DLL\n" \
    "  :type data: bytes (Python 3.x) or str (Python 2.x)\n" \
    "\n" \
    "  :return: Handle of loaded EXE/DLL\n" \
    "  :rtype: PyCapsule<HMEMORYMODULE> or CObjects (Python 2.6)\n"

#define DOCSTRING_MemoryGetProcAddress "MemoryGetProcAddress(module, name):\n" \
    "\n" \
    "Get address of exported function.\n" \
    "\n" \
    "Supports loading both by name and by ordinal value\n" \
    "\n" \
    "  :param module: Handle of loaded EXE/DLL as HMEMORYMODULE\n" \
    "  :type module: PyCapsule<HMEMORYMODULE> or CObjects (Python 2.6)\n" \
    "  :param name: Name or ordinal value of exported function\n" \
    "  :type name: str\n" \
    "\n" \
    "  :return: Address of function\n" \
    "  :rtype: ctypes.c_void_p\n"

#define DOCSTRING_MemoryFreeLibrary "MemoryFreeLibrary(module):\n" \
    "\n" \
    "Free previously loaded EXE/DLL.\n" \
    "\n" \
    "  :param module: Handle of loaded EXE/DLL as HMEMORYMODULE\n" \
    "  :type module: PyCapsule<HMEMORYMODULE> or CObjects (Python 2.6)\n"

static PyObject* _MemoryLoadLibrary(PyObject* self, PyObject* args)
{
    void* data;
    size_t size;
    HMEMORYMODULE handle;

    if (!PyArg_ParseTuple(args, READONLY_BUFFER, &data, &size)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    handle = MemoryLoadLibrary(data, size);
    Py_END_ALLOW_THREADS

    if (!handle) {
        PyErr_SetFromWindowsErr(GetLastError());
        return NULL;
    }

    return PyCapsule_New(handle, "HMEMORYMODULE", NULL);
}

static PyObject* _MemoryGetProcAddress(PyObject* self, PyObject* args)
{
    PyObject* module;
    char* name;
    HMEMORYMODULE handle;
    FARPROC address;

    if (!PyArg_ParseTuple(args, "Os", &module, &name)) {
        return NULL;
    }

    handle = PyCapsule_GetPointer(module, "HMEMORYMODULE");
    if (!handle) {
        PyErr_SetString(
            PyExc_TypeError,
            "module must be PyCapsule<HMEMORYMODULE> or CObjects  (Python 2.6)"
        );
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    address = MemoryGetProcAddress(handle, name);
    Py_END_ALLOW_THREADS

    if (!address) {
        PyErr_SetFromWindowsErr(GetLastError());
        return NULL;
    }

    return PyObject_CallFunction(
        c_void_p,
        "O",
        PyLong_FromVoidPtr(address)
    );
}

static PyObject* _MemoryFreeLibrary(PyObject* self, PyObject* args)
{
    PyObject* module;
    HMEMORYMODULE handle;

    if (!PyArg_ParseTuple(args, "O", &module)) {
        return NULL;
    }

    handle = PyCapsule_GetPointer(module, "HMEMORYMODULE");
    if (!handle) {
        PyErr_SetString(
            PyExc_TypeError,
            "module must be PyCapsule<HMEMORYMODULE> or CObjects  (Python 2.6)"
        );
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    MemoryFreeLibrary(handle);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

/*
 * Initialization module
 */

static PyMethodDef methods[] = {
    {"MemoryLoadLibrary", (PyCFunction)_MemoryLoadLibrary,
        METH_VARARGS, DOCSTRING_MemoryLoadLibrary},
    {"MemoryGetProcAddress", (PyCFunction)_MemoryGetProcAddress,
        METH_VARARGS, DOCSTRING_MemoryGetProcAddress},
    {"MemoryFreeLibrary", (PyCFunction)_MemoryFreeLibrary,
        METH_VARARGS, DOCSTRING_MemoryFreeLibrary},
    {NULL, NULL, 0, NULL}   /* sentinel */
};

#if PY_MAJOR_VERSION >= 3
    #define INIT_FUNC PyInit_pymemorymodule
    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "pymemorymodule",
        NULL,
        -1,
        methods,
    };
#else
    #define INIT_FUNC initpymemorymodule
#endif

PyMODINIT_FUNC INIT_FUNC(void)
{
    PyObject *ctypes = PyImport_ImportModule("ctypes");
    c_void_p = PyObject_GetAttrString(ctypes, "c_void_p");

#if PY_MAJOR_VERSION >= 3
    return PyModule_Create(&module);
#else
    Py_InitModule("pymemorymodule", methods);
#endif
}
