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
#include <sys/uio.h>
#include "aio.h"
#ifdef SPINLOCK
    static ck_spinlock_t submitLock = CK_SPINLOCK_INITIALIZER;
#endif
/*
 * event should have predefined timeout and can return 0
 * which should be ignored
 */

/*
 * this call should not be used directly
 * execute IO request
 * there can be only IO read or IO write submitted for whole request
 * mixed types are not supported
 */
long int executeAio(Taiofile *self,   TaioctxIoRequest *request)
{
        unsigned int lastIndex, i;
        long int status;
        char *bufferPointer;
        TaioctxCallback *callback;
        struct iovec *iov = NULL;
        struct iocb *job = NULL;
        struct iocb **job_request;
        size_t totalNrOfChunks;
        int ret;

        i = 0;
        totalNrOfChunks = getMaxNrOfChunks(request->allocInfo);
        bufferPointer = request->pyBuffer->buf;
        lastIndex = totalNrOfChunks - 1;
        job = malloc(sizeof(struct iocb));
        if (job == NULL)
        {
                free(request);
                PyErr_SetString(PyExc_MemoryError, " Can't allocate job buffer");
                return CALL_FAILED;
        }
        // allocate callbacks structure
        callback = malloc(totalNrOfChunks * sizeof(TaioctxCallback));
        if (callback == NULL)
        {
                PyErr_SetString(PyExc_MemoryError, " Can't allocate callback buffer");
                free(job);
                free(request);
                return CALL_FAILED;
        }

        job_request = &job;

        if (lastIndex > 0) {
                iov = malloc(totalNrOfChunks * sizeof(struct iovec));
                // setup callback for every request
                for (i=0; i<lastIndex; i++)
                {
                        iov[i].iov_base = bufferPointer;
                        iov[i].iov_len = request->allocInfo->blockSize;
                        bufferPointer += request->allocInfo->blockSize;
                }
        }
        callback->fd = self->fd;
        callback->flags = request->ioType;
        callback->defered = request->defer;
        callback->fileOffset = &self->offset;
        callback->fileSize = &self->size;
        callback->pyBuffer = request->pyBuffer;
        callback->objectBuffer = request->objectBuffer;
        callback->ioSize = request->ioSize;
        //free pointers
        callback->extraBuffer = request->extraBuffer;
        callback->freeJobPointer = job;
        callback->freeCallbackPointer = callback;
        if (request->allocInfo->nrOfBytesToCopy == 0)
        {
                switch(request->ioType)
                {
                case READ_EVENT:
                        if (!iov) {
                                // need to check return
                                debug("single aligned read %ld size\n",request->allocInfo->lastBlockSize);
                                io_prep_pread(job, self->fd,  bufferPointer, request->allocInfo->blockSize, self->offset);
                        }
                        else {
                                // add last vector
                                debug("vector aligned read %d entries\n",i);
                                iov[i].iov_base = bufferPointer;
                                iov[i].iov_len = request->allocInfo->blockSize;
                                // need to check return
                                io_prep_preadv(job, self->fd, iov, totalNrOfChunks, self->offset);
                        }
                        break;
                case WRITE_EVENT:
                        if (!iov) {
                                // check return
                                debug("single aligned write %ld size\n",request->allocInfo->lastBlockSize);
                                io_prep_pwrite(job, self->fd,  bufferPointer, request->allocInfo->blockSize, self->offset);
                        }
                        else {
                                debug("vector aligned write %d entries\n",i);
                                // last vector
                                iov[i].iov_base = bufferPointer;
                                iov[i].iov_len = request->allocInfo->blockSize;
                                // check return
                                io_prep_pwritev(job, self->fd, iov, totalNrOfChunks, self->offset);
                        }
                        break;
                default:
                        free(request);
                        if(iov)
                                free(iov);
                        return CALL_FAILED;
                }
        }
        else
        {
                // for write we need to point to different buffer
                switch(request->ioType)
                {
                case READ_EVENT:
                        if (!iov) {
                                debug("single non aligned read %ld size\n",request->allocInfo->lastBlockSize);
                                io_prep_pread(job, self->fd,  bufferPointer, request->allocInfo->lastBlockSize, self->offset);
                        }
                        else {
                                debug("vector not aligned read  %d entries\n",i);
                                iov[i].iov_base = bufferPointer;
                                iov[i].iov_len = request->allocInfo->blockSize;
                                io_prep_preadv(job, self->fd, iov, totalNrOfChunks, self->offset);
                        }
                        break;
                case WRITE_EVENT:
                        if (!iov) {
                                debug("single not aligned write %ld size\n",request->allocInfo->lastBlockSize);
                                io_prep_pwrite(job, self->fd,  request->extraBuffer, request->allocInfo->lastBlockSize, self->offset);
                        }
                        else {
                                debug("vector not aligned write  %d entries %ld size\n",i, request->allocInfo->lastBlockSize);
                                iov[i].iov_base = callback->extraBuffer;
                                iov[i].iov_len = request->allocInfo->lastBlockSize;
                                io_prep_pwritev(job, self->fd, iov, totalNrOfChunks, self->offset);
                        }
                        break;
                default:
                        free(request);
                        if(iov)
                                free(iov);
                        return CALL_FAILED;
                }
        }
        // assign callback to job
        job->data = (void *)callback;
        // connect eventfile with job
        debug("set eventfd start\n");
        io_set_eventfd(job, self->eventfd);
        debug("set event complete\n");
        // at this point we have all io jobs prepared
        // and proper callbacks attached
        // we can now submit them
        if (!self->ctx) {
                if (callErrback(request->defer, PyExc_IOError, -2, NULL) == 0) {
                        status = CALL_FAILED;
                }
                else {
                        status =  CALL_ERRBACK;
                }
        }
        else {
                Py_BEGIN_ALLOW_THREADS;
#ifdef SPINLOCK
                ck_spinlock_lock(&submitLock);
                ret = io_submit(*self->ctx, 1, job_request);
                ck_spinlock_unlock(&submitLock);
#else
                ret = io_submit(*self->ctx, 1, job_request);
#endif
                Py_END_ALLOW_THREADS;
                debug("submit complete  with status %d\n", ret);
                status = ret;
                if (ret < 1) {
                        // most likely wee need to clean stuff here
                        // submit failed
                        // call errback
                        if (status ==  -EAGAIN) {
                                ret = callErrback(request->defer, TaIoError, IGNORE_ME_ERROR, "AGAIN");
                        }
                        else
                                ret = callErrback(request->defer,PyExc_IOError, IGNORE_ME_ERROR, strerror(ret * -1));
                        if (ret == 0) {
                                status = CALL_FAILED;
                        }
                        else {
                                status =  CALL_ERRBACK;
                        }
                }
        }
        debug("FREE REQUEST\n");
        free(request);
        debug("FREE IOV\n");
        if (iov) {
                free(iov);
        }
        return status;
}

/*
 * open file
 */
int open_file(char const* file, int flags, int mode)
{
        int fd = open(file, flags, mode);
        return fd;
}

/*
 * calculate aligned size based on provided size
 */
size_t  getAlignedSizeDifference(size_t size)
{
        return (size % PAGE_SIZE);
}

/*
 * get number of chunks
 */

size_t getMaxNrOfChunks( TaioctxAllocInfo *allocInfo)
{
        size_t totalNrOfChunks = 0;
        if (allocInfo->nrOfBytesToCopy != 0)
        {
                // we are unaligned
                // create proper buffer size
                totalNrOfChunks = allocInfo->nrOfChunks + 1;
        }
        else
        {
                totalNrOfChunks = allocInfo->nrOfChunks;
        }
        return totalNrOfChunks;
}
/*
 *  get buffer size
 */
size_t getBufferSize( TaioctxAllocInfo *allocInfo)
{
        size_t bufferSize = 0;
        if (allocInfo->nrOfBytesToCopy != 0)
        {
                // we are unaligned
                // create proper buffer size
                bufferSize = allocInfo->blockSize * allocInfo->nrOfChunks + allocInfo->lastBlockSize;
        }
        else
        {
                bufferSize = allocInfo->blockSize * allocInfo->nrOfChunks;
        }
        return bufferSize;
}

/*
 * Check memory allocation
 */

int checkMemoryAllocation(void *pointer)
{

        if (pointer ==  NULL)
        {
                PyErr_SetString(PyExc_MemoryError, strerror(errno));
                return 0;
        }
        return 1;
}
/*
 *  calculate align block based on provided size
 */
TaioctxAllocInfo *checkAllignedSize(size_t size, int directIO)
{

        TaioctxAllocInfo *allocInfo;
        allocInfo = malloc(sizeof(TaioctxAllocInfo));
        int blockSize, i;
        if (allocInfo == NULL)
        {
                return NULL;
        }
        // lets calculate biggest possible block
        // starting from 4K ending on 1MB
        for(i=0; i<=8; i++)
        {
                blockSize =  (4<<i) * 1024;
                // if size == 2 * blockSize
                // our blockSize == blockSize
                // ex. 7Kb <  2*4K so blockSize == 4K
                if (size < 2 * blockSize)
                {
                        break;
                }
        }
        // wecalculated biggest available blockSize
        // for size > 1MB 1MB is our max blockSize
        allocInfo->blockSize = blockSize;
        // calculate how many full chunks we have
        allocInfo->nrOfChunks =  size / allocInfo->blockSize;
        // at this point we have proper number of chunks
        // and we need to calculate how many bytes are left
        allocInfo->nrOfBytesToCopy = size % allocInfo->blockSize;
        allocInfo->lastBlockSize = 0;
        // let calculate what will be smallest block in which we will fit
        // remaining block bytes
        if (allocInfo->nrOfBytesToCopy > 0)
        {
                if (directIO) {
                        for(i=0; i<=8; i++)
                        {
                                allocInfo->lastBlockSize = (4<<i) * 1024;
                                if (allocInfo->nrOfBytesToCopy < allocInfo->lastBlockSize)
                                {
                                        break;
                                }
                        }
                }
                else {
                        allocInfo->lastBlockSize = allocInfo->nrOfBytesToCopy;
                }
        }
        return allocInfo;
}


int processEvent(Taioctx *self)
{
        struct io_event *events;
        struct io_event *ep;
        int n, iter, success, ret;
        TaioctxCallback *callback;
        PyObject *arglist= NULL;
        PyObject *result = NULL;
        PyObject *py_deferred = NULL;
        struct timespec tmo;
        iter = self->max_requests;
        size_t currentOffset;
        size_t previousOffset;
        // memory allocation
        events = malloc(iter * sizeof(struct io_event));
        if (events == NULL)
        {
                self->active = 0;
                PyErr_SetString(PyExc_MemoryError," Can't allocate event buffer");
                return -1;
        }
        success = -1;
        tmo.tv_sec = 0;
        tmo.tv_nsec = 0;
        /*
         * get up to aio_maxio events at a time.
         */
        n = io_getevents(*self->ctx, 1, iter, events, &tmo);
        success = n;
        /*
         * Call the callback functions for each event.
         */
        for (ep = events; n-- > 0; ep++)
        {
                callback = (TaioctxCallback *)ep->data;
                py_deferred = PyObject_GetAttrString(callback->defered, "callback");
                previousOffset = *callback->fileOffset;
                currentOffset = *callback->fileOffset + callback->ioSize;
                if (callback->flags == WRITE_EVENT)
                {
                        if (currentOffset > *callback->fileSize) {
                                *callback->fileSize = currentOffset;
                        }
                        *callback->fileOffset = currentOffset;
                        arglist = Py_BuildValue("(l)", callback->ioSize);
                        result = PyEval_CallObject(py_deferred, arglist);
                        if (result == NULL) {
                                success = -1;
                                PyErr_SetString(PyExc_RuntimeError,"Failed to call write callback\n");
                                *callback->fileOffset = previousOffset;
                                if (previousOffset < *callback->fileSize) {
                                        *callback->fileSize = previousOffset;
                                }
                        }
                }
                else if (callback->flags == READ_EVENT)
                {
                        PyBuffer_Release(callback->pyBuffer);
                        if (PyByteArray_Size(callback->objectBuffer) < callback->ioSize)
                                ret = PyByteArray_Resize(callback->objectBuffer, callback->ioSize);
                        else
                                ret = 1;
                        if (ret) {
                                arglist = Py_BuildValue("(O)", callback->objectBuffer);
                                if (arglist == NULL) {
                                        success = -1;
                                        PyErr_SetString(PyExc_RuntimeError,"Failed to build read arguments\n");
                                        Py_XDECREF(callback->objectBuffer);
                                        Py_XDECREF(callback->pyBuffer);
                                        break;
                                }
                                *callback->fileOffset = currentOffset;
                                result = PyEval_CallObject(py_deferred, arglist);
                                if (result == NULL) {
                                        success = -1;
                                        PyErr_SetString(PyExc_RuntimeError,"Failed to call read callback\n");
                                        *callback->fileOffset = previousOffset;
                                        Py_XDECREF(callback->objectBuffer);
                                        Py_XDECREF(callback->pyBuffer);
                                        break;
                                }
                        }
                        else
                        {
                                PyErr_Clear();
                                if (callErrback(callback->defered, PyExc_RuntimeError, IGNORE_ME_ERROR, "Array Resize failed") == 0) {
                                        PyErr_SetString(PyExc_RuntimeError,"Array Resize failed");
                                        success = -1;
                                        Py_XDECREF(callback->objectBuffer);
                                        Py_XDECREF(callback->pyBuffer);
                                        break;
                                }
                                success = 0;
                        }
                        Py_XDECREF(callback->objectBuffer);
                        Py_XDECREF(callback->pyBuffer);
                }
                else
                {
                        arglist = Py_BuildValue("(l)", -1);
                        if (arglist == NULL) {
                                PyErr_SetString(PyExc_RuntimeError,"Failed to call sync argument\n");
                                success = -1;
                        }
                        result = PyEval_CallObject(py_deferred, arglist);
                        if (result == NULL) {
                                PyErr_SetString(PyExc_RuntimeError,"Failed to call sync callback\n");
                                success = -1;
                        }
                }
                // free lists as this is last request
                if (arglist)
                        Py_DECREF(arglist);
                if (result)
                        Py_DECREF(result);
                if (py_deferred)
                        Py_DECREF(py_deferred);
                if (callback->defered)
                        Py_DECREF(callback->defered);
                if (callback->extraBuffer)
                        free(callback->extraBuffer);
                callback->extraBuffer = NULL;
                //free(callback->freeJobRequestPointer);
                free(callback->freeJobPointer);
                free(callback->freeCallbackPointer);
        }
        // do cleaning
        free(events);
        if (success < 0)
                return 0;
        return 1;
}


int checkIfValidOffset(size_t fileSize, size_t ioSize, size_t offset, int ioType, int directIO) {
        int result  = 0;
        switch (ioType) {
        case READ_EVENT:
                if (ioSize + offset <= fileSize) {
                        result = 1;
                }
                break;
        case WRITE_EVENT:
                debug("write fileOffset: %ld fileSize: %ld ioSize: %ld\n", offset, fileSize, ioSize);
                if (ioSize + offset > fileSize) {
                        result = 1;
                }
                if (ioSize  + offset > 0) {
                        result = 1;
                }
                break;
        default:
                result = 0;
                break;
        }
        if (ioSize <= 0) {
                result  = 0;
        }
        return result;
}
