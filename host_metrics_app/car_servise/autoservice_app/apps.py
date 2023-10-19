from django.apps import AppConfig


class AutoserviceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservice_app'

    def ready(self):
        from . import signals
