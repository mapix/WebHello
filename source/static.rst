======
Static
======

API Reference
=============

.. py:module:: WebHello.static

.. py:class:: Static(self, application, static_config, rewrite_rule=None)

   Serve static

   .. py:attribute:: application

   .. py:attribute:: url_prefix

   .. py:attribute:: directory_prefix

   .. py:attribute:: rewrite_rule

   .. py:method:: __call__(self, environ, start_response)

   .. py:method:: serve_static(self, environ, start_response)
