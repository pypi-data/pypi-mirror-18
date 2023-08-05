=============================
Django Balystic
=============================


.. image:: https://badge.fury.io/py/django-balystic.png
    :target: https://badge.fury.io/py/django-balystic

.. image:: https://travis-ci.org/inqbation/django-balystic.png?branch=master
    :target: https://travis-ci.org/inqbation/django-balystic

Connect to Balystic API in your Django project



Quickstart
----------

Install Django Balystic::

    pip install django-balystic

Then use it in a project::

    import balystic


Features
--------

This client makes it easy to use the balystic API.
Just add a couple settings::

    BALYSTIC_API_TOKEN = 'mysecrettoken'
    BALYSTIC_API-PATH = 'mycommunity.7dhub.com/api/'

Then create a client instance::

    from balystic.client import Client
    client = Client()

And use the client to perform the requests::

    user_list = client.get_users()
    user_detail = client.get_user_detail()
    client.delete_user()


A couple of views have been defined to display information
from your community.

blogs:

::
    blog/    | template name = blog_list.html
    blog/<slug>/ | template name = blog_detail.html

qa:

::
    qa/ | template_name = qa_list.html
    qa/<pk>/ | template_name= qa_detail.html

to modify the template, create a folder in your project template folder called
** balystic ** with the same name of the used inside the balystic app.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
