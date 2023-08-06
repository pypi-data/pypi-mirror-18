Django Form Renderers
=====================

**Sometimes form.as_p doesn't cut it. This app adds more render methods to all forms.**

.. figure:: https://travis-ci.org/praekelt/django-form-renderers.svg?branch=develop
   :align: center
   :alt: Travis

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``django-form-renderers`` to your Python path.

#. Add ``form_renderers`` to your ``INSTALLED_APPS`` setting.

What it does
------------

#. Every form receives a div-based render method called ``as_div``.

#. If a field is required then an attribute ``required="required"`` is rendered for every widget.
   This is a safe blanket assumption.

#. Optional - every field and input gets extra BEM CSS classes.

Defining your own renderers
---------------------------

Create either ``form_renderers.py`` or ``form_renderers/__init__.py`` in your app. Each renderer must
be a function::

    def as_some_renderer(form):
        return form._html_output(
            ...
        )

    def as_another_renderer(form):
        return form._html_output(
            ...
        )


You can override the default ``as_div`` by creating a renderer called ``as_div`` in your app.
The same rules that apply for Django template overriding apply to renderer overriding.

BEM
---

BEM is a CSS naming convention that advocates explicit naming over inheritance. Django
forms, fields and widgets are not BEM aware. To enabled BEM classes from settings do::

    FORM_RENDERERS = {"enable-bem-classes": True}

