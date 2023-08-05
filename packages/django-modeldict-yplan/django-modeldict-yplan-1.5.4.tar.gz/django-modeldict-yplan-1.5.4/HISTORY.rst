.. :changelog:

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
