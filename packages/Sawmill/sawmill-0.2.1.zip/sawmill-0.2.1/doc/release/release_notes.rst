..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _release/release_notes:

*************
Release Notes
*************

.. release:: 0.2.1
    :date: 2016-11-08

    .. change:: fixed

        :meth:`RedirectToSawmillHandler.emit
        <sawmill.compatibility.RedirectToSawmillHandler.emit>` calls target
        handle method with incorrect arguments.

.. release:: 0.2.0
    :date: 2016-07-11

    .. change:: new

        Added :mod:`compatibility <sawmill.compatibility>` helpers for
        redirecting standard :mod:`logging` to Sawmill.

    .. change:: changed

        Included :mod:`configurators <sawmill.configurator>` now redirect
        standard library logging to Sawmill. This can be turned off by passing
        ``redirect_standard_logging=False`` to the configurator.

.. release:: 0.1.1
    :date: 2016-06-08

    .. change:: fixed

        Exceptions raised on
        :meth:`~sawmill.handler.stream.Stream.teardown` of
        :class:`~sawmill.handler.stream.Stream` handler if underlying stream was
        already closed as part of cleanup process.

    .. change:: changed
        :tags: documentation

        Simplified documentation structure.

    .. change:: fixed
        :tags: documentation

        Added missing :ref:`installing` section.

    .. change:: fixed
        :tags: documentation

        Fixed broken documentation references.

    .. change:: changed

        :meth:`Log.__repr__ <sawmill.log.Log.__repr__>` updated to return useful
        and accurate representation of :class:`Log <sawmill.log.Log>` instances.

    .. change:: fixed

        Refactored ``test_stream:test_auto_flush_on_exit`` that caused incorrect
        code coverage results to be reported.

.. release:: 0.1.0
    :date: 2016-05-25
    
    .. change:: new

        Initial release for evaluation.
