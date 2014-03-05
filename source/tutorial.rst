========
WebHello
========
.. image:: https://github.com/mapix/WebHello/raw/81adfdb467b4fd176ff0c61c3f4946e8d1874157/examples/todolist/static/favicon.ico

Yet-another micro web framework in Python.

`WebHello` is a micro web framework written completely to demonstrate how common web framework works. Components include:

* Http Request support cookie and other useful method to interact with `WSGI` environ.
* Simple Http Response generate.
* Http Exception handle.
* Simple static file serving.
* Http Router supported by regular expression.
* HTML Template implemented by regular expression totally.

Installing
==========
Install `WebHello` from source::

    git clone https://github.com/mapix/WebHello.git
    cd WebHello
    python setup.py install

Using `WebHello`
================
Hello world example, Checkout Examples_ for more information.

.. _Examples: https://github.com/mapix/WebHello/tree/master/examples

app.py::
    
    from WebHello.static import Static
    from WebHello.router import Router

    application = Router(urls)
    urls = [('/', 'hello:say_hello'), ('/{mame:\w+}', 'hello:say_hello')]
    rewrites = {'/favicon.ico': '/static/favicon.ico'}
    application = Static(application, ('/static/', 'static'), rewrites)

    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8000, application)
        print "Serving on port 8000..."
        httpd.serve_forever()

hello.py::

    def say_hello(request, name="mapix"):
        return "hello %s" % mapix

License
========
**WebHello** is copyright 2013 mapix and Contributors, and is made available under BSD-style license; see LICENSE_ for details.

.. _LICENSE: https://github.com/mapix/WebHello/blob/master/LICENSE
