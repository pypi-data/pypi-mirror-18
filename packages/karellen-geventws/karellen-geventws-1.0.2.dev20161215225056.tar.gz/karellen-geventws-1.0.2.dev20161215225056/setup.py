#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'karellen-geventws',
        version = '1.0.2.dev20161215225056',
        description = '''Karellen Gevent Websocket Library''',
        long_description = '''Karellen Gevent Websocket Library
=================================

This is a `Karellen <https://www.karellen.co/karellen/>`__ fork of
`gevent-websocket <http://www.bitbucket.org/Jeffrey/gevent-websocket/>`__.
The goal of this fork is to maintain the project to support Python 3.3,
3.4 and 3.5+ as well as latest WS standards errata.

`karellen-geventws <https://github.com/karellen/karellen-geventws/>`__
is a WebSocket library for the `gevent <http://www.gevent.org/>`__
networking library.

Features include:

-  Integration on both socket level or using an abstract interface.
-  RPC and PubSub framework using `WAMP <http://wamp-proto.org>`__
   (WebSocket Application Messaging Protocol).
-  Easily extendible using a simple WebSocket protocol plugin API

.. code:: python


        from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

        class EchoApplication(WebSocketApplication):
            def on_open(self):
                print("Connection opened")

            def on_message(self, message):
                self.ws.send(message)

            def on_close(self, reason):
                print(reason)

        WebSocketServer(
            ('', 8000),
            Resource({'/': EchoApplication})
        ).serve_forever()

or a low level implementation:

.. code:: python


        from gevent import pywsgi
        from geventwebsocket.handler import WebSocketHandler

        def websocket_app(environ, start_response):
            if environ["PATH_INFO"] == '/echo':
                ws = environ["wsgi.websocket"]
                message = ws.receive()
                ws.send(message)

        server = pywsgi.WSGIServer(("", 8000), websocket_app,
            handler_class=WebSocketHandler)
        server.serve_forever()

More examples can be found in the ``src/unittest/python`` directory.
Hopefully more documentation will be available soon.

Installation
============

The easiest way to install karellen-geventws is directly from
`PyPi <https://pypi.python.org/pypi/karellen-geventws/>`__ using pip or
setuptools by running the commands below:

::

    $ pip install karellen-geventws

Gunicorn Worker
---------------

Using Gunicorn it is even more easy to start a server. Only the
websocket\_app from the previous example is required to start the
server. Start Gunicorn using the following command and worker class to
enable WebSocket funtionality for the application.

::

    gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" wsgi:websocket_app

Performance
-----------

`karellen-geventws <https://github.com/karellen/karellen-geventws/>`__
is pretty fast, but can be accelerated further by installing
`wsaccel <https://github.com/methane/wsaccel>`__ and ``ujson`` or
``simplejson``:

::

    $ pip install wsaccel ujson

`karellen-geventws <https://github.com/karellen/karellen-geventws/>`__
automatically detects ``wsaccel`` and uses the Cython implementation for
UTF8 validation and later also frame masking and demasking.

Get in touch
------------

The fork parent is located at
`gevent-websocket <http://www.bitbucket.org/Jeffrey/gevent-websocket/>`__.

Issues can be created on
`GitHub <https://github.com/karellen/karellen-geventws/issues>`__.
''',
        author = "Jeffrey Gelens, Karellen, Inc",
        author_email = "jeffrey@noppo.pro, supervisor@karellen.co",
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/karellen/karellen-geventws',
        scripts = [],
        packages = [
            'geventwebsocket',
            'geventwebsocket.gunicorn',
            'geventwebsocket.protocols'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Internet'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['gevent'],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
        keywords='',
    )
