from celery import Task

from ct_core_api.core.task_queue import celery


def init_app(app):
    # Only configure the Celery extension if a connection URL is set
    if not bool(app.config.get('CELERY_BROKER_URL')):
        return

    class AppContextAwareTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return Task.__call__(self, *args, **kwargs)

    celery.main = app.import_name
    celery.task_cls = AppContextAwareTask
    celery.conf.update(app.config)

    app.register_extension(celery)
