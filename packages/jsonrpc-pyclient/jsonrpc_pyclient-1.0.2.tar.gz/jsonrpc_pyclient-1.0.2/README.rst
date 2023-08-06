jsonrpc_pyclient
================
jsonrpc_pyclient is a transport-agnostic json-rpc 2.0 and 1.0 client library primarily intended for use with
libjson-rpc-cpp_ but can be used with other json-rpc server implementations.

.. _libjson-rpc-cpp: https://github.com/cinemast/libjson-rpc-cpp

This library is intended to be used with libjson-rpc-cpp's stubgenerator,
which takes a json-formatted specification file, and can then return server
and client stubs in various languages; the python client stub generator was
created to use this library. For more information on using the stubgenerator,
refer to libjson-rpc-cpp's documentation.

Currently Supported Transports
------------------------------
- http
- tcp sockets


Basic Usage
-----------
.. code-block:: python

    >>> from jsonrpc_pyclient.connectors import socketclient
    >>> import ClientStub #client stub created by libjson-rpc-cpp stubgenerator
    >>> connector = socketclient.TcpSocketClient("127.0.0.1", 8032)
    >>> client = ClientStub(connector)
    >>> result = client.addNumbers(4, 5)
    >>> print(result)


Installation
------------
.. code-block:: bash

    $ pip install jsonrpc_pyclient
