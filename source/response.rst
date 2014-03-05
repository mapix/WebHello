========
Response
========

.. py:module:: WebHello.response

.. py:class:: Response(output='', request=None)

   Http Response

    .. py:attribute:: output

    .. py:attribute:: request

    .. py:attribute:: cookies

    .. py:attribute:: response_headers

    .. py:method:: set_cookie(self, name, value, domain=None, path='/', expires=None, max_age=None, secure=None, httponly=None, version=None)

    .. py:method:: __call__(self, environ, start_response)
