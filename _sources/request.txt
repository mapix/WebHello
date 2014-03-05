=======
Request
=======

API Reference
=============

.. py:module:: WebHello.request

.. py:class:: Request(environ)

    Http Request

    .. py:attribute:: environ

    .. py:attribute:: config

    .. py:attribute:: files

    .. py:attribute:: params

    .. py:attribute:: cookies
       

    .. py:method:: get_cookie(self, name)

    .. py:method:: get_var(self, name, default=None)

    .. py:method:: get_list_var(self, name)

    .. py:method:: get_method(self)

    .. py:method:: get_path_info(self)

    .. py:method:: get_scheme(self)

    .. py:method:: get_url(self)

    .. py:method:: get_upload_type(self, name)

    .. py:method:: get_upload_content(self, name)

       get upload content as a string.

       :param str name: field name of the file input
       :rtype: str
