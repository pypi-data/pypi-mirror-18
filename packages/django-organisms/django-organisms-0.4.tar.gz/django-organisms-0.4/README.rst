=========
Organisms
=========

Organisms is a simple Django app to represent organisms.


Download and Install
--------------------

This package is registered as "django-organisms" in PyPI and is pip
installable:

.. code-block:: shell

  pip install django-organisms

If ``django`` is not found on your system, ``pip`` will install it too.


Quick Start
-----------

1. Add **'organisms'** to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
        ...
        'organisms',
    )

2. Run ``python manage.py migrate`` command to create ``organisms`` model.

3. **(Optional)** The following step is only needed if you have
   django-tastypie installed to create a REST API for your project and
   would like to have API endpoints for ``django-organisms``.

   Add the following to your project's ``urls.py`` file:

   ::

    # There are probably already other imports here, such as:
    # from django.conf.urls import url, patterns, include
 
    # If you have not already done so, import the tastypie API:
    from tastypie.api import Api
 
    # Import the OrganismResource:
    from organisms.api import OrganismResource
 
    # If you have not already done so, initialize your API and
    # add the OrganismResource to it
    v0_api = Api()
    v0_api.register(OrganismResource())
 
    # In the urlpatterns, include the urls for this api:
    urlpatterns = patterns('',
        ...
        (r'^api/', include(v0_api.urls))
    )


Usage of Management Command
---------------------------

This app includes a management command
``management/commands/organisms_create_or_update.py``,
which can be used to populate the organisms table in the database.
It takes 3 arguments:

* taxonomy_id
* scientific_name
* common_name

For example, to populate the Human object in the database, we would enter:

.. code-block:: shell

  python manage.py organisms_create_or_update --taxonomy_id=9606 --scientific_name="Homo sapiens" --common_name="Human"
