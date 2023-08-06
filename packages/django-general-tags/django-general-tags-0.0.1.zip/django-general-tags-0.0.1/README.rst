=====
Django-General-Tags
=====

django-general-tags is a liberary of useful custom django tags.

With django-general-tags you can develop django applications faster and 
easier, and no need to deal with some difficult stuff about tags and filters.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "generaltags" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'generaltags',
    ]

2. Load the general_tags filter in your templates like this::

    {% load general_tags %}
