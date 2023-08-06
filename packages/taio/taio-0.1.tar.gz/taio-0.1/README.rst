taio
-----------------

Implementing asynchronous I/O for Twisted 

Basic implementation of asychronous IO calls for Twisted.

Twisted have excelent non blocking I/O library however actual I/O operations
still working in synch mode.
This library removes that limitation.

It using native linux aio ( as posix aio thread mode interference with twisted in some cases)
and provides simple interface for reads and writes 

