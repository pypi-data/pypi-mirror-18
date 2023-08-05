==========
Change Log
==========

0.3
===

* Removed dependency on *setuptools* (`Issue #4`_)
* Added support for classes as request validators (as opposed to entry point
  names)
* Added ability to customize applications by overriding methods:

  * :py:meth:`~milla.app.Application.make_request`
  * :py:meth:`~milla.app.Application.resolve_path`
  * :py:meth:`~milla.app.Application.handle_error`

* Added :py:class:`~milla.controllers.HTTPVerbController`
* Removed deprecated ``milla.cli``
* Removed deprecated ``milla.dispatch.routing.Generator``

0.2.1
=====

* Fixed trailing slash redirect with empty path inf (`Issue #7`_)
* Fixed a compatibility issue with some servers and ``HEAD`` responses
* Allow specifying ``allowed_methods`` on controller classes

0.2
===

* Python 3 support
* Added new utility functions:

  * :py:func:`~milla.util.http_date`
  * :py:func:`~milla.util.read_config`

* Added :py:meth:`~milla.Request.static_resource`
* Corrected default handling of HTTP ``OPTIONS`` requests (`Issue #5`_)
* Deprecated :py:mod:`milla.cli`
* Deprecated :py:class:`~milla.dispatch.routing.Generator` in favor of
  :py:meth:`~milla.Request.create_href`

0.1.2
=====

* Improvements to :py:class:`~milla.controllers.FaviconController` (`Issue
  #1`_)

0.1.1
=====

* Fixed a bug when generating application-relative URLs with
  :py:class:`~milla.routing.dispatch.URLGenerator`:

0.1
===

Initial release

.. _Issue #1: https://bitbucket.org/AdmiralNemo/milla/issue/1
.. _Issue #5: https://bitbucket.org/AdmiralNemo/milla/issue/5
.. _Issue #7: https://bitbucket.org/AdmiralNemo/milla/issue/7
.. _Issue #4: https://bitbucket.org/AdmiralNemo/milla/issue/4
