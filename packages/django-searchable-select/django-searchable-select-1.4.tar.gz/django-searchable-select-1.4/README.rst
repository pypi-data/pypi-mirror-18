django-searchable-select
========================

A better and faster multiple selection widget with suggestions for
Django

What is this?
=============

This plugin provides a replacement for standard multi-choice select on
Django admin pages.

You can use this as custom widget for ``ManyToManyField``.

Features
========

-  Filtering is performed on server side and thus significantly improves
   performance.
-  Uses ``Twitter Typeahead`` to provide suggestion completion.
-  Works **great** with ManyToMany fields that can be chosen from
   thousands of thousands of choices, e. g. ``User - City`` relations.

Before
~~~~~~

.. figure:: https://habrastorage.org/files/dd9/f17/87e/dd9f1787e0dd4e05826fdde08e270609.png
   :alt: Before

   Before

After
~~~~~

.. figure:: https://habrastorage.org/files/db2/c87/460/db2c87460992470e9d8e19da307c169d.png
   :alt: Before

   Before

Installation
============

1. Install ``django-searchable-select``.

   .. code:: sh

       $ pip install django-searchable-select

2. Add ‘searchableselect’ to your settings.

   .. code:: python

       # settings.py

       INSTALLED_APPS = (
           # ...
           'searchableselect',
           # ...
       )

3. Add URL pattern required for the suggesting engine to your root
   ``urls.py``.

   .. code:: python

       # urls.py

       urlpatterns = patterns(
           '',
           # ...
           url('^searchableselect/', include('searchableselect.urls')),
           # ...
       )

4. Use the widget in your model admin class:

   .. code:: python

       from django import models, forms
       from models import MyModel

       class MyModelForm(forms.ModelForm):
           class Meta:
               model = models.MyModel
               exclude = ()
               widgets = {
                   'cities': SearchableSelect(model='cities.City', search_field='name', many=True)
               }


       class MyModelAdmin(admin.ModelAdmin):
           form = Form

       admin.site.register(models.MyModel, MyModelAdmin)

   Remember to **always** initialize ``SearchableSelect`` with three
   keyword arguments: ``model``, ``search_field`` and ``many``.

   -  ``model`` is the string in form ``APP_NAME.MODEL_NAME``
      representing your model in the project, e. g. ‘cities.City’
   -  ``search_field`` is the field within model that will be used to
      perform filtering, e. g. ‘name’
   -  ``many`` must be ``True`` for ``ManyToManyField`` and ``False``
      for ``ForeignKey``.

Known issues
============

- Not tested with empty fields.

Contributing
============

I’m looking forward to bug reports and any kind of contribution.

License
=======

You are free to use this where you want as long as you keep the author
reference. Please see LICENSE for more info.
