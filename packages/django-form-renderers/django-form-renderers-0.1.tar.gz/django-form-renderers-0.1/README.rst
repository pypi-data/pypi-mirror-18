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

Coming soon
-----------

User definable render methods.

