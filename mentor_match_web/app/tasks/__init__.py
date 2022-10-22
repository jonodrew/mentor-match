from app.extensions import celery_app


def make_celery(app):
    celery_app.conf.update(app.config)
    celery_app.conf.imports = ("app.tasks.tasks",)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
