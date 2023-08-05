================
django-modeldict
================

.. image:: https://img.shields.io/pypi/v/django-modeldict-yplan.svg
    :target: https://pypi.python.org/pypi/django-modeldict-yplan

.. image:: https://travis-ci.org/YPlan/django-modeldict.svg?branch=master
    :target: https://travis-ci.org/YPlan/django-modeldict


``ModelDict`` is a very efficient way to store things like settings in your database. The entire model is transformed into a dictionary (lazily) as well as stored in your cache. It's invalidated only when it needs to be (both in process and based on ``CACHE_BACKEND``).

It was originally created by `Disqus <https://github.com/disqus/django-modeldict>`_, but due to the inactivity we at YPlan have taken over maintenance on this fork.

Requirements
------------

Tested with all combinations of:

* Python: 2.7, 3.5
* Django: 1.8, 1.9, 1.10

Install
-------

Install it with **pip**:

.. code-block:: bash

    pip install django-modeldict-yplan

Make sure you ``pip uninstall django-modeldict`` first if you're upgrading from the original to this fork - the packages clash.

Example Usage
-------------

.. code-block:: python

    # You'll need a model with fields to use as key and value in the dict
    class Setting(models.Model):
        key = models.CharField(max_length=32)
        value = models.CharField(max_length=200)

    # Create the ModelDict...
    settings = ModelDict(Setting, key='key', value='value', instances=False)

    # And you can treat it like a normal dict:

    # Missing values = KeyError
    settings['foo']
    >>> KeyError

    # Sets supported
    settings['foo'] = 'hello'

    # Fetch the current value using normal dictionary access
    settings['foo']
    >>> 'hello'

    # ...or by normal model queries
    Setting.objects.get(key='foo').value
    >>> 'hello'




=======
History
=======

Pending release
---------------

* New release notes here

1.5.4 (2016-10-28)
------------------

* Fixed a race condition in threaded code. See https://github.com/YPlan/django-modeldict/pull/40 for a detailed
  explanation. Thanks @Jaidan.

1.5.3 (2016-09-20)
------------------

* Stop rounding ``time.time()`` down to the nearest integer, so we are more fine grained around expiration. It might
  also fix a subtle timing bug around re-fetching the remote cache unnecessarily.

1.5.2 (2016-07-31)
------------------

* Fixed update missing when ``_local_last_updated`` could be set even when it
  wasn't updated
* Fixed update missing from integer rounding in time comparison
* Fixed ``CachedDict.__repr__`` so it works for other subclasses of
  ``CachedDict`` than ``ModelDict`` (don't assume ``self.model`` exists)

1.5.1 (2016-06-13)
------------------

* Fixed local cache never expiring if value was checked too often.
* Use Django's ``cache.set_many`` for more efficient storage.

1.5.0 (2016-01-11)
------------------

* Forked by YPlan
* Fixed concurrency TOCTTOU bug for threaded Django servers.
* Stopped including the 'tests' directory in package
* Django 1.8 and 1.9 supported.
* Python 3 support added.
* Fixed ``setdefault()`` to return the value that was set/found, as per normal dict semantics. Thanks @olevinsky.

1.4.1 (2012-12-04)
------------------

* Last release by Disqus


