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



/*
 * deallocate File object
 */
static void
Taiofile_dealloc(Taiofile* self)
{
        close(self->fd);
        self->ob_type->tp_free((PyObject*)self);
}

/*
 * Create  new File object
 */
static PyObject *
Taiofile_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
        Taiofile *self;
        self = (Taiofile *)type->tp_alloc(type, 0);
        if (self == NULL)
        {
                // failed to allocate object
                return NULL;
        }
        return (PyObject *)self;
}

static PyObject*
Taiofile_getfd(Taiofile *self, void *closure)
{
        return Py_BuildValue("i", self->fd);
}

static PyObject*
Taiofile_setro(Taiofile *self, void *closure)
{
        PyErr_SetString(PyExc_TypeError, "Attribute is read-only!");
        return NULL;

}


/*
 * Init File object
 */

static int
Taiofile_init(Taiofile *self, PyObject *args, PyObject *kwds)
{
        PyObject *ctx;
        int ret;
        static char *kwlist[] = {"ctx", "fd", "eventfd", "directIO",NULL};
        struct stat f_stat;

        // parse kwargs
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oiii", kwlist, &ctx, &self->fd, &self->eventfd, &self->directIO))
        {
                return -1;
        }
        self->ctx = (io_context_t *)PyCapsule_GetPointer(ctx,"ctx");
        Py_DECREF(ctx);
        self->offset = 0;
        Py_BEGIN_ALLOW_THREADS;
        ret = fstat(self->fd, &f_stat);
        Py_END_ALLOW_THREADS;
        if (ret < 0) {
                PyErr_SetString(PyExc_IOError, strerror(errno));
                return -1;
        }
        self->size = f_stat.st_size;
        return 0;
}

static PyMethodDef Taiofile_methods[] =
{
        {"read", (PyCFunction)Taiofile_read, METH_VARARGS|METH_KEYWORDS, "read"},
        {"write", (PyCFunction)Taiofile_write, METH_VARARGS|METH_KEYWORDS, "write"},
        {"seek", (PyCFunction)Taiofile_seek, METH_VARARGS|METH_KEYWORDS, "seek"},
        {"tell", (PyCFunction)Taiofile_tell, METH_NOARGS, "tell"},
        {"close", (PyCFunction)Taiofile_close, METH_NOARGS, "close"},
        {"__enter__", (PyCFunction)Taiofile_enter, METH_NOARGS, "enter"},
        {"__exit__", (PyCFunction)Taiofile_exit, METH_VARARGS, "exit"},
        {NULL} /* Sentinel */
};

static PyGetSetDef Taiofile_getseters[] = {
        {   "fd", (getter)Taiofile_getfd, (setter)Taiofile_setro,
            "file descriptor", NULL},
        {NULL} /* Sentinel */
};

static PyMemberDef Taiofile_members[] =
{
        {
                "size", T_LONG, offsetof(Taiofile, size), 1,
                "size"
        },
        {
                "offset", T_LONG, offsetof(Taiofile, offset), 1,
                "offset"
        },
        {NULL} /* Sentinel */
};


PyTypeObject taiofile_Type =
{
        PyObject_HEAD_INIT(NULL)
        0,                        /*ob_size*/
        "taio.taioFile",            /*tp_name*/
        sizeof(Taiofile),         /*tp_basicsize*/
        0,                        /*tp_itemsize*/
        (destructor)Taiofile_dealloc, /*tp_dealloc*/
        0,                        /*tp_print*/
        0,                        /*tp_getattr*/
        0,                        /*tp_setattr*/
        0,                        /*tp_compare*/
        0,                        /*tp_repr*/
        0,                        /*tp_as_number*/
        0,                        /*tp_as_sequence*/
        0,                        /*tp_as_mapping*/
        0,                        /*tp_hash */
        0,                        /*tp_call*/
        0,                        /*tp_str*/
        0,                        /*tp_getattro*/
        0,                        /*tp_setattro*/
        0,                        /*tp_as_buffer*/
        Py_TPFLAGS_DEFAULT,       /*tp_flags*/
        "TaIO file object",       /* tp_doc */
        0,                        /* tp_traverse */
        0,                        /* tp_clear */
        0,                        /* tp_richcompare */
        0,                        /* tp_weaklistoffset */
        0,                        /* tp_iter */
        0,                        /* tp_iternext */
        Taiofile_methods,         /* tp_methods */
        Taiofile_members,         /* tp_members */
        Taiofile_getseters,       /* tp_getset */
        0,                        /* tp_base */
        0,                        /* tp_dict */
        0,                        /* tp_descr_get */
        0,                        /* tp_descr_set */
        0,                        /* tp_dictoffset */
        (initproc)Taiofile_init,  /* tp_init */
        0,                        /* tp_alloc */
        Taiofile_new,             /* tp_new */
};
