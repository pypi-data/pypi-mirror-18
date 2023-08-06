#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <signal.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>
#include <sys/eventfd.h>
#include <linux/version.h>
#include <stdarg.h>
#include "aio.h"


static PyMethodDef module_methods[] =
{
        {NULL} /* Sentinel */
};

/*
 *
 */
int callErrback(PyObject *defer, PyObject *error, int errorNumber, const char *fmt, ...)
{
        PyObject *errback, *attrlist, *exception, *ret;
        va_list arg;
        errback = PyObject_GetAttrString(defer, "errback");
        if (errback == NULL)
        {
                if (errorNumber == IGNORE_ME_ERROR)
                {
                        va_start(arg,fmt);
                        PyErr_Format(error, fmt, arg);
                        va_end(arg);
                }
                else
                {
                        PyErr_Format(error, "Failed to set errback: %s", strerror(errorNumber));
                }
                return 0;
        }
        if (errorNumber == IGNORE_ME_ERROR)
        {
                va_start(arg, fmt);
                attrlist = Py_BuildValue("(O)", PyString_FromFormat(fmt, arg));
                va_end(arg);
        }
        else
        {
                attrlist = Py_BuildValue("(O)", PyString_FromFormat("%s", strerror(errorNumber)));
        }
        exception = PyEval_CallObject(error, attrlist);
        if (exception == NULL)
        {
                if (errorNumber == IGNORE_ME_ERROR)
                {
                        va_start(arg, fmt);
                        PyErr_Format(PyExc_MemoryError, fmt, arg);
                        va_end(arg);
                }
                else
                {
                        PyErr_Format(PyExc_MemoryError, "Failed to set exception in errback: %s", strerror(errorNumber));
                }
                return 0;
        }
        attrlist = Py_BuildValue("(O)", exception);
        ret = PyEval_CallObject(errback, attrlist);
        if (ret == NULL)
        {
                return 0;
        }
        Py_XDECREF(ret);
        Py_XDECREF(defer);
        Py_XDECREF(attrlist);
        Py_XDECREF(exception);
        Py_XDECREF(errback);
        return 1;
}

/*
 * call deferred errback with specific error number and information
 *
 */
PyObject  *callCallback(PyObject *defer, PyObject *value)
{
        PyObject *callback, *attrlist, *ret;
        callback = PyObject_GetAttrString(defer, "callback");
        if (callback == NULL)
        {
                PyErr_Format(PyExc_MemoryError, "Out of mem");
                return NULL;
        }
        attrlist = Py_BuildValue("(O)", value);
        ret = PyEval_CallObject(callback, attrlist);
        if (ret == NULL)
        {
                PyErr_Format(PyExc_TypeError, "can't call callback");
                return NULL;
        }
        Py_XDECREF(ret);
        Py_XDECREF(defer);
        Py_XDECREF(attrlist);
        Py_XDECREF(callback);
        return defer;
}


PyObject *
init_taio(void)
{
        PyObject *m;
        PyObject *__version__;

        __version__ = PyString_FromFormat("%s", TAIO_VERSION);
        if (!__version__)
        {
                return NULL;
        }

        m = Py_InitModule3("core", module_methods, NULL);
        if (!m)
        {
                Py_DECREF(__version__);
                return NULL;
        }

        if (PyModule_AddObject(m, "__version__", __version__))
        {
                Py_DECREF(__version__);
                Py_DECREF(m);
                return NULL;
        }
        // mian ctx object
        taioctx_Type.tp_new = PyType_GenericNew;
        if (PyType_Ready(&taioctx_Type) < 0)
        {
                Py_DECREF(__version__);
                Py_DECREF(m);
                return NULL;
        }

        Py_INCREF(&taioctx_Type);
        PyModule_AddObject(m, "taioContext", (PyObject *)&taioctx_Type);

        // main file object
        taiofile_Type.tp_new = PyType_GenericNew;
        if (PyType_Ready(&taiofile_Type) < 0)
        {
                Py_DECREF(__version__);
                Py_DECREF(m);
                return NULL;
        }

        Py_INCREF(&taiofile_Type);
        PyModule_AddObject(m, "taioFile", (PyObject *)&taiofile_Type);

        // twisted types
        PyObject *defer;
        defer = PyImport_ImportModule("twisted.internet.defer");
        if (defer == NULL)
        {
                Py_DECREF(&taioctx_Type);
                Py_DECREF(&taiofile_Type);
                Py_DECREF(__version__);
                Py_DECREF(m);
                return NULL;
        }

        Deferred = PyObject_GetAttrString(defer, "Deferred");
        if (Deferred == NULL)
        {
                PyErr_SetString(PyExc_ImportError, "Can not import twisted.internet.defer.Deferred.");
                Py_DECREF(defer);
                Py_DECREF(&taioctx_Type);
                Py_DECREF(&taiofile_Type);
                Py_DECREF(__version__);
                Py_DECREF(m);
                return NULL;
        }

        //exceptions
        TaIoError = PyErr_NewException("taio.taioError", NULL, NULL);
        Py_INCREF(TaIoError);
        PyModule_AddObject(m, "taioError", TaIoError);
        return m;
}

PyMODINIT_FUNC initcore(void)
{
        init_taio();
}
