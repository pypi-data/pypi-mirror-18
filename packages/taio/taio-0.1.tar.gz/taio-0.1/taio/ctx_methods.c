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

#define PAGE_SIZE 4096


/*
 * display if context status ( 1 active , 0 inactive)
 */
PyObject *Taioctx_active(Taioctx* self)
{
        int active;
        active = self->active;
        return Py_BuildValue("i", active);
}



/*
 * send write request
 */

void destroy_ctx_pointer(PyObject* ctx) {
        PyCapsule_SetContext(ctx, NULL);
}


/*
 * open file
 * return taio.File object
 */
PyObject*
Taioctx_open(Taioctx *self, PyObject *args, PyObject *kwds)
{
        PyObject  *path, *arglist, *fileObj;
        int flags = O_CREAT|O_RDWR|O_TRUNC;
        int mode = S_IRWXU|S_IRWXG|S_IROTH;
        int fd = -1;
        int directIO;
        static char *kwlist[] = {"path", "flags", "mode", NULL};
        PyObject *capsule;

        // parse kwargs
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|ii", kwlist, &path, &flags, &mode))
        {
                return NULL;
        }
        if (PyString_Check(path))
        {
                // open file and throw error if required
                Py_INCREF(path);
                const char* cPath = PyString_AsString(path);
                fd = open_file(cPath, flags, mode);
                if(fd < 0)
                {
                        PyErr_SetString(PyExc_IOError, strerror(errno));
                        Py_DECREF(path);
                        return NULL;
                }
                Py_DECREF(path);
                flags = fcntl(fd, F_GETFL, 0);
                if (!(flags & O_NONBLOCK))
                {
                        fcntl(fd, F_SETFL, flags | O_NONBLOCK);
                }
        }
        if (!(flags & O_DIRECT)) {
                directIO = 0;
        }
        else {
                directIO = 1;
        }
        capsule = PyCapsule_New((void *) self->ctx, "ctx", destroy_ctx_pointer);
        arglist = Py_BuildValue("(Oiii)",capsule, fd, self->fd, directIO);
        if (arglist == NULL)
                return NULL;
        fileObj = PyObject_CallObject((PyObject *)&taiofile_Type, arglist);
        Py_DECREF(arglist);
        if (fileObj == NULL)
                return NULL;
        return fileObj;
}


/*
 * stop ctx
 */
PyObject*
Taioctx_stop(Taioctx *self)
{
        int rc;
        rc = close(self->fd);
        if(rc < 0)
        {
                Py_RETURN_FALSE;
        }
        Py_RETURN_TRUE;
}

PyObject *Taioctx_event(Taioctx *self)
{
        int ret;
        ret = processEvent(self);
        switch (ret)
        {
        case 1:
                Py_RETURN_TRUE;
                break;
        default:
                return NULL;
        }
        return NULL;
}


PyObject*
Taioctx_fileno(Taioctx *self)
{
        return PyInt_FromLong(self->fd);
}
