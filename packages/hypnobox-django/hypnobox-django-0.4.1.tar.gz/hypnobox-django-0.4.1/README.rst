=============================
hypnobox-django
=============================

.. image:: https://badge.fury.io/py/hypnobox-django.png
    :target: https://badge.fury.io/py/hypnobox-django

.. image:: https://travis-ci.org/fgmacedo/hypnobox-django.png?branch=master
    :target: https://travis-ci.org/fgmacedo/hypnobox-django

Integrate your site with Hypnobox chat service.

Documentation
-------------

The full documentation is at https://hypnobox-django.readthedocs.org.

Quickstart
----------

Install hypnobox-django::

    pip install hypnobox-django

Include it on `INSTALLED_APPS`::

    'hypnobox',

And in your routes (`urls.py`)::

    url(r'^leads/', include('hypnobox.urls', namespace='hypnobox')),

Then use it in a template:

.. code-block:: django

    {% load hypnobox_tags  %}
    {% new_lead "your-product-code" "your-media-name" %}


It will render a link to a :ref:`LeadForm`, and on submiting this form, it
will persist a lead and redirect the user to Hypnobox chat.

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py
