========
Template
========

.. py:module:: WebHello.template

.. py:class:: Lookup(template_base, **config)

    .. py:attribute:: template_base
    .. py:attribute:: config

    .. py:method:: search_template(self, template_file)

    .. py:method:: serve_template(self, template_file, **kwargs)

    .. py:method:: serve_template_func(self, template_file, block, **kwargs)


.. py:class:: Template(environ)

    .. py:attribute:: lookup
    .. py:attribute:: filename
    .. py:attribute:: raw_source
    .. py:attribute:: parent

    .. py:method:: render(self, namespace)


Supported syntax
================

* Evaluation Statement::

    {= title =}
    {= len(users) + len(groups) =}

* Loop Statement::

    {% for user in users %}
      <tr>
        <td>{= loop.index =}</td>
        <td><a href="{= user.url() =}">{= user.name =}</a></td>
      </tr>
    {% endfor %}

* IF Statement::
   
    {% if user.is_admin() or user.is_manager() %}
        Welcome {= user.name =}
    {% elif user.active() %}
        Ha, ha. You are active.
    {% else %}
      {% for food in foods %}
         <li>{= loop.index =}. choice {= food =}
      {% endfor %}
    {% endif %}


* Inlucde Statement::

    {* include "widgets/nav.html" (group="this is group", action=action) *}

* Page Args::
    
    {@ group, action, name="this is name" @}

* Block Definition::

    {% block show_block(q, user="user") %}
      <p>==============
      <p>this is show_block in base.html
      <P>q is {= q =}
      <p>user is {= user =}
      <p>==============
    {% endblock %}

* Block Invocation::

    {$show_block('<this is q>', '<this is user>')$}

* Template Inherit::

    {^ base="base.html" ^}

