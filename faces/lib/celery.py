# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from celery.app import shared_task
from celery.app.task import Task


def faces_task(**kwargs):
    """
    Decorator that passes any kwargs as ``_custom_options`` to the celery task.
    Celery will then magically assign ``_custom_options`` as property to the celery task instance.
    See: http://celery.readthedocs.org/en/latest/userguide/tasks.html#list-of-options
    """
    def decorator(fn):
        return shared_task(bind=True, base=FacesTask, _custom_options=kwargs)(fn)
    return decorator


class FacesTask(Task):
    """
    Custom base task for all of our celery tasks

    - asserts that tasks are delayed with proper task execution context
    - provides ``custom_options``, which can be provided as kwargs to the ``faces_task`` decorator
    """
    abstract = True

    @property
    def custom_options(self):
        if not hasattr(self, '_custom_options'):
            return {}

        return self._custom_options

    def delay(self, *args, **kwargs):
        context = kwargs.pop("context", None)
        return self.apply_async(args, kwargs, headers={
            "context": context
        })
