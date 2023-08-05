==========
gwebsocket
==========

`gwebsocket`_ is a WebSocket library for the gevent_ networking library.

::

    from gevent import pywsgi
    from gwebsocket.handler import WebSocketHandler

    def websocket_app(environ, start_response):
        if environ["PATH_INFO"] == '/echo':
            ws = environ["wsgi.websocket"]
            message = ws.receive()
            ws.send(message)

    server = pywsgi.WSGIServer(("", 8000), websocket_app,
        handler_class=WebSocketHandler)
    server.serve_forever()

Installation
------------

The easiest way to install gwebsocket is directly from PyPi_ using pip or
setuptools by running the commands below::

    $ pip install gwebsocket


Gunicorn Worker
^^^^^^^^^^^^^^^

Using Gunicorn it is even more easy to start a server. Only the
`websocket_app` from the previous example is required to start the server.
Start Gunicorn using the following command and worker class to enable WebSocket
funtionality for the application.

::

    gunicorn -k "gwebsocket.gunicorn.GWebSocketWorker" wsgi:websocket_app

Performance
^^^^^^^^^^^

`gwebsocket`_ is pretty fast, but can be accelerated further by
installing `wsaccel <https://github.com/methane/wsaccel>`_ and `ujson` or `simplejson`::

    $ pip install wsaccel ujson

`gwebsocket`_ automatically detects ``wsaccell`` and uses the Cython
implementation for UTF8 validation and later also frame masking and demasking.

Get in touch
^^^^^^^^^^^^

Issues can be created
at `Bitbucket <https://bitbucket.org/btubbs/gwebsocket/issues?status=new&status=open>`_.

Acknowledgements
^^^^^^^^^^^^^^^^

gwebsocket is based on `Jeffrey Gelens`_' `gevent-websocket`_.
gwebsocket omits gevent-websocket's WAMP features and WebSocketApplication mini
framework, in favor of providing just a minimal library for use in other
frameworks.  gwebsocket also makes it possible to do cleanup on close without
building your app as a WebSocketApplication.

.. _gwebsocket: http://www.bitbucket.org/btubbs/gwebsocket/
.. _gevent: http://www.gevent.org/
.. _Jeffrey Gelens: http://www.gelens.org/
.. _PyPi: http://pypi.python.org/pypi/gevent-websocket/
.. _repository: http://www.bitbucket.org/Jeffrey/gevent-websocket/
.. _RFC6455: http://datatracker.ietf.org/doc/rfc6455/?include_text=1
