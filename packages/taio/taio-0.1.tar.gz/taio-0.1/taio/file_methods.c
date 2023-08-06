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


#define SECTOR_SIZE 4096

/*
 * send read request
 */

PyObject*
Taiofile_read(Taiofile *self, PyObject *args, PyObject *kwds)
{

        PyObject *attrlist, *defer, *objectBuffer;
        Py_buffer *bufferView;
        TaioctxAllocInfo *allocInfo = NULL;
        size_t readSize, bufferSize;
        TaioctxIoRequest *ioRequest = NULL;
        long status;

        static char *kwlist[] = {"size",  NULL};
        readSize = 0;
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "|l", kwlist, &readSize))
        {
                return NULL;
        }
        Py_XDECREF(args);
        if (self->fd < 0)
        {
                PyErr_SetString(PyExc_TypeError, "file descriptor not exists -1");
                return NULL;
        }
        attrlist = Py_BuildValue("()");
        if (attrlist == NULL) {
                return NULL;
        }
        defer = PyInstance_New(Deferred, attrlist, NULL);
        if (defer == NULL) {
                Py_XDECREF(attrlist);
                return NULL;
        }
        Py_XINCREF(defer);
        Py_XDECREF(attrlist);

        if (checkIfValidOffset(self->size, 0, self->offset, READ_EVENT, self->directIO))
        {
                // we reached end of file
                free(ioRequest);
                return callCallback(defer, Py_BuildValue(""));
        }

        bufferView = malloc(sizeof(Py_buffer));
        if (!checkMemoryAllocation(bufferView))
        {
                return NULL;
        }
        ioRequest  = malloc(sizeof(TaioctxIoRequest));
        if (!checkMemoryAllocation(ioRequest))
        {
                free(bufferView);
                return NULL;
        }
        if (readSize == 0)
        {
                readSize = self->size;
                if (readSize == 0)
                {
                        Py_XDECREF(defer);
                        free(bufferView);
                        free(ioRequest);
                        return callCallback(defer, Py_BuildValue(""));
                }
                if (self->offset > 0)
                        readSize = readSize - self->offset;
        }
        else if (self->offset > 0 && self->offset % SECTOR_SIZE != 0 && self->directIO)
        {
                // now we need to check if offset is aligned
                PyErr_SetString(PyExc_TypeError, "offset must be aligned with sector boundary");
                return NULL;
        }
        // this is shity need to do some extra calculations
        if (!(checkIfValidOffset(self->size, readSize, self->offset, READ_EVENT, self->directIO)))
        {
                free(bufferView);
                free(ioRequest);
                return callCallback(defer, Py_BuildValue(""));
        }
        allocInfo = checkAllignedSize(readSize, self->directIO);
        if (!checkMemoryAllocation(ioRequest))
        {
                PyErr_SetString(PyExc_MemoryError, "offset must be aligned with sector boundary");
                Py_XDECREF(defer);
                free(bufferView);
                free(ioRequest);
                return NULL;
        }
        bufferSize = getBufferSize(allocInfo);
        objectBuffer = PyByteArray_FromStringAndSize(NULL, bufferSize);
        status = PyObject_GetBuffer(objectBuffer, bufferView, PyBUF_CONTIG);
        if (status < 0)
        {
                // error is set by getBuffer
                Py_XDECREF(defer);
                free(bufferView);
                free(ioRequest);
                free(allocInfo);
                return NULL;
        }
        debug("create read AIO %lu\n",readSize);
        // create IO Request
        ioRequest->objectBuffer = objectBuffer;
        ioRequest->pyBuffer = bufferView;
        ioRequest->allocInfo = allocInfo;
        ioRequest->ioType = READ_EVENT;
        ioRequest->defer = defer;
        ioRequest->extraBuffer = NULL;
        ioRequest->ioSize = readSize;
        status = executeAio(self, ioRequest);
        switch (status)
        {
        case CALL_ERRBACK:
                Py_XDECREF(objectBuffer);
                free(bufferView);
                free(allocInfo);
                break;
        case CALL_FAILED:
                Py_XDECREF(objectBuffer);
                free(bufferView);
                free(allocInfo);
                return NULL;
                break;
        default:
                free(allocInfo);
        }
        return defer;
}


/*
 * send write request
 */
PyObject*
Taiofile_write(Taiofile *self, PyObject *args, PyObject *kwds)
{
        PyObject *attrlist, *objectBuffer;
        PyObject *defer = NULL;

        Py_buffer *bufferView = NULL;
        int status;

        TaioctxAllocInfo *allocInfo = NULL;
        char *bufferPointer = NULL;
        char *extraBuffer = NULL;
        long int totalNrOfChunks;
        static char *kwlist[] = {"buffer", NULL};
        TaioctxIoRequest *ioRequest = NULL;

        // parse keywords
        Py_XINCREF(args);
        if (PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &objectBuffer))
        {
                if (!PyObject_CheckBuffer(objectBuffer))
                {
                        PyErr_SetString(PyExc_TypeError, "write buffer must support buffer interface");
                        return NULL;
                }
                Py_XINCREF(objectBuffer);
        }
        else
        {
                return NULL;
        }
        Py_XDECREF(args);

        // create main defered
        attrlist = Py_BuildValue("()");
        if (attrlist == NULL) {
                return NULL;
        }
        defer = PyInstance_New(Deferred, attrlist, NULL);
        if (defer == NULL) {
                Py_XDECREF(attrlist);
                return NULL;
        }
        Py_XINCREF(defer);
        Py_XDECREF(attrlist);

        bufferView = malloc(sizeof(Py_buffer));
        if (!checkMemoryAllocation(bufferView))
        {
                Py_XDECREF(defer);
                return NULL;
        }
        /* Get a Buffer INCREF */
        PyObject_GetBuffer(objectBuffer, bufferView, PyBUF_CONTIG_RO);
        if (bufferView->len <= 0)
        {
                // we will not use defer in processing so we can decrease ref
                Py_XDECREF(defer);
                free(bufferView);
                return callCallback(defer, PyInt_FromLong(0));
        }
        if (!(checkIfValidOffset(self->size, bufferView->len, self->offset, WRITE_EVENT, self->directIO))) {
                PyErr_SetString(PyExc_TypeError, "offset incorrect");
                Py_XDECREF(defer);
                free(bufferView);
                return NULL;
        }
        // let's calculate how many blocks/chunks do we need
        // and check if last chunk is aligned
        allocInfo = checkAllignedSize(bufferView->len, self->directIO);
        if (!checkMemoryAllocation(allocInfo))
        {
                Py_XDECREF(defer);
                free(bufferView);
                return NULL;
        }
        // fallocate space for file
        if (self->offset + bufferView->len > self->size)
        {
                fallocate(self->fd, 0, 0, bufferView->len + self->offset);
        }
        if (allocInfo->nrOfBytesToCopy > 0)
        {
                ///  me need to do some memcopy :( , as last chunks was not aligned
                // blockSize
                bufferPointer = bufferView->buf;
                bufferPointer += (bufferView->len - allocInfo->nrOfBytesToCopy);
                // allocate and memcpy data from RO buffer_view to extra block
                // we just need to copy actual bytes and not to worry about
                // remaining content of extarBuffer as file will be truncated
                // after last write request
                extraBuffer = malloc(allocInfo->lastBlockSize * sizeof(char));
                if (!checkMemoryAllocation(extraBuffer))
                {
                        Py_XDECREF(defer);
                        free(allocInfo);
                        free(bufferView);
                }
                memcpy(extraBuffer, bufferPointer, allocInfo->nrOfBytesToCopy);
        }
        else
        {
                extraBuffer = NULL;
        }
        //  lets calculate total number of chunks
        totalNrOfChunks = getMaxNrOfChunks(allocInfo);
        // funny - it was zero length write requests
        if (totalNrOfChunks == 0)
        {
                // if we reached this point something is wrong
                PyErr_SetString(PyExc_IOError, "nothing to write\n");
                Py_XDECREF(defer);
                free(allocInfo);
                free(bufferView);
                if (extraBuffer)
                {
                        free(extraBuffer);
                }
                return NULL;
        }
        ioRequest  = malloc(sizeof(TaioctxIoRequest));
        if (!checkMemoryAllocation(ioRequest))
        {
                Py_XDECREF(defer);
                free(allocInfo);
                free(bufferView);
                if (extraBuffer)
                {
                        free(extraBuffer);
                }
                return NULL;
        }
        ioRequest->pyBuffer = bufferView;
        ioRequest->allocInfo = allocInfo;
        ioRequest->ioType = WRITE_EVENT;
        ioRequest->defer = defer;
        ioRequest->ioSize = bufferView->len;
        ioRequest->extraBuffer = extraBuffer;
        status = executeAio(self, ioRequest);
        switch (status)
        {
        case CALL_ERRBACK:
                free(allocInfo);
                free(bufferView);
                if (extraBuffer)
                {
                        free(extraBuffer);
                }
                break;
        case CALL_FAILED:
                //Py_XDECREF(defer);
                free(allocInfo);
                free(bufferView);
                if (extraBuffer)
                {
                        free(extraBuffer);
                }
                return NULL;
                break;
        default:
                free(allocInfo);
                break;
        }
        return defer;
}


/*
 * close file
 */
PyObject*
Taiofile_close(Taiofile *self)
{
        int rc;

        // parse kwargs
        rc = close(self->fd);
        if (rc < 0)
        {
                Py_RETURN_FALSE;
        }
        self->offset = 0;
        self->size = 0;
        self->fd = -1;
        Py_RETURN_TRUE;
}

/*
 * tell call
 */
PyObject*
Taiofile_tell(Taiofile *self)
{
        return PyInt_FromLong(self->offset);
}

/*
 * seek file
 */
PyObject*
Taiofile_seek(Taiofile *self, PyObject *args, PyObject *kwds)
{
        long long temp_offset = -1;
        static char *kwlist[] = {"offset", NULL};
        Py_XINCREF(args);
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "|l", kwlist, &temp_offset))
        {
                return NULL;
        }
        Py_XDECREF(args);
        if (temp_offset >= 0)
        {
                self->offset = temp_offset;
        }
        return PyInt_FromLong(self->offset);
}
/*
 * __enter__
 */
PyObject*
Taiofile_enter(Taiofile *self)
{
        Py_INCREF(self);
        return (PyObject *)self;
}

/*
 *  __exit__
 */
PyObject*
Taiofile_exit(Taiofile *self, PyObject *args)
{
        close(self->fd);
        self->offset = 0;
        self->size = 0;
        self->fd = -1;
        Py_RETURN_NONE;
}
