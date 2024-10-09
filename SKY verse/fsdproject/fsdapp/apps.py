from django.apps import AppConfig

class FsdappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fsdapp'

    def ready(self):
        import fsdapp.signals
