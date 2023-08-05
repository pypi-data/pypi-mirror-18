Welcome to pytest-django-ahead!
===============================

This is a fork from `pytest-django <https://github.com/pytest-dev/pytest-django>`_ where I pick some PR's that
I find important for my current work. This is not the official pytest-django package, but rather a package that origins
from a release tag, and where changesets from PR's in the project that has not yet been released are merged in.

Any important documentation, with exclusion of the ones listed below (that are not yet apart of pytest-django's
released packages).


Features included that are not in pytest-django 3.0.0
-----------------------------------------------------

`An mailoutbox function scoped fixture, that provides a list of mails sent out from django <https://github.com/pytest-dev/pytest-django/pull/410>`_
`An autouse function scoped fixture, that clears django.contrib.sites.models.SITE_CACHE from keeping cached entries <https://github.com/pytest-dev/pytest-django/pull/323>`_


Travis
------

You can find build reports by checking the `3.0.0-ahead branch from here <https://travis-ci.org/dolphinkiss/pytest-django/branches>`_.


Install pytest-django
---------------------

::

    pip install pytest-django-ahead

