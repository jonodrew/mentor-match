from app.extensions import celery


def make_celery(app):
    celery.conf.update(app.config)
    celery.conf.imports = ("app.tasks.tasks",)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
