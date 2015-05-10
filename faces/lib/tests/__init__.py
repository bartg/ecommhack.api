# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from django.test.utils import override_settings
from nose.tools.nontrivial import make_decorator


def with_celery(eager=True, propagate_exceptions=True):
    """
    Decorator for test cases which execute celery tasks.

    If this decorator is applied, all delayed celery tasks are run synchronously in the main execution thread
    and exceptions thrown by these tasks are also propagated and thrown in the main thread.
    """
    def decorator(fn):
        @override_settings(CELERY_ALWAYS_EAGER=eager, CELERY_EAGER_PROPAGATES_EXCEPTIONS=propagate_exceptions)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return make_decorator(fn)(wrapper)
    # Will preserve nose metadata
    return decorator