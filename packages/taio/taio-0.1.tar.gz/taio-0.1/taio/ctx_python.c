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


static char Taioctx_active_docstring[] =
        "Display active state";

static char Taioctx_open_docstring[] =
        "open file";

static char Taioctx_stop_docstring[] =
        "stop ctx";

static char Taioctx_event_docstring[] =
        "process ctx event";

static char Taioctx_fileno_docstring[] =
        "return event fileno";


/*
 * deallocate CTX object
 */
static void
Taioctx_dealloc(Taioctx* self)
{
        if (self->ctx) {
                io_destroy(*self->ctx);
                free(self->ctx);
                self->ctx = NULL;
        }
        self->ob_type->tp_free((PyObject*)self);
}

/*
 * Create  new CTX object
 */
static PyObject *
Taioctx_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
        Taioctx *self;
        self = (Taioctx *)type->tp_alloc(type, 0);
        if (self != NULL)
        {
                self->fd = -1;
                self->max_requests = 128;
                self->active = 0;
        }
        else
        {
                // failed to allocate object
                return NULL;
        }
        return (PyObject *)self;
}


/*
 * Init CTX object
 */

static int
Taioctx_init(Taioctx *self, PyObject *args, PyObject *kwds)
{
        int ret;
        //int i;
        //struct rlimit rlim;

        static char *kwlist[] = {"max_requests",  NULL};
        // parse kwargs
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &self->max_requests))
        {
                return -1;
        }
        self->ctx =  malloc(sizeof(io_context_t));
        if(!checkMemoryAllocation(self->ctx))
                return -1;
        //
        // set max IO requests if it's not set
        if(self->max_requests <= 0)
        {
                self->max_requests = 128;
        }
        memset(self->ctx, 0, sizeof(io_context_t));
        ret = io_setup(self->max_requests, self->ctx);
        if (self->ctx) {
        }
        if (ret != 0)
        {
                PyErr_SetString(PyExc_IOError, strerror(ret));
                return -1;
        }

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,27)
        if ((self->fd = eventfd(0,0)) == -1)
        {
#else
        if ((self->fd = eventfd(0,EFD_NONBLOCK|EFD_SEMAPHORE)) == -1)
        {
#endif
                PyErr_SetString(PyExc_IOError, strerror(errno));
                io_destroy(*self->ctx);
                free(self->ctx);
                return -1;
        }
        self->active=1;
        return 0;
}

static PyMethodDef Taioctx_methods[] =
{
        {"active", (PyCFunction)Taioctx_active, METH_NOARGS,Taioctx_active_docstring},
        {"open", (PyCFunction)Taioctx_open, METH_VARARGS|METH_KEYWORDS, Taioctx_open_docstring},
        {"stop", (PyCFunction)Taioctx_stop, METH_NOARGS, Taioctx_stop_docstring},
        {"event", (PyCFunction)Taioctx_event, METH_NOARGS, Taioctx_event_docstring},
        {"fileno", (PyCFunction)Taioctx_fileno, METH_NOARGS, Taioctx_fileno_docstring},
        {NULL} /* Sentinel */
};


static PyMemberDef Taioctx_members[] =
{
        {
                "max_requests", T_INT, offsetof(Taioctx, max_requests), 1,
                "max requests"
        },
        {NULL} /* Sentinel */
};


PyTypeObject taioctx_Type =
{
        PyObject_HEAD_INIT(NULL)
        0,                        /*ob_size*/
        "taio.taioContext",         /*tp_name*/
        sizeof(Taioctx),          /*tp_basicsize*/
        0,                        /*tp_itemsize*/
        (destructor)Taioctx_dealloc, /*tp_dealloc*/
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
        "TaIO context object",    /* tp_doc */
        0,                        /* tp_traverse */
        0,                        /* tp_clear */
        0,                        /* tp_richcompare */
        0,                        /* tp_weaklistoffset */
        0,                        /* tp_iter */
        0,                        /* tp_iternext */
        Taioctx_methods,          /* tp_methods */
        Taioctx_members,          /* tp_members */
        0,                        /* tp_getset */
        0,                        /* tp_base */
        0,                        /* tp_dict */
        0,                        /* tp_descr_get */
        0,                        /* tp_descr_set */
        0,                        /* tp_dictoffset */
        (initproc)Taioctx_init,   /* tp_init */
        0,                        /* tp_alloc */
        Taioctx_new,              /* tp_new */
};
