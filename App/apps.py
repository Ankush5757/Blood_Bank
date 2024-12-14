from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'App'

    def ready(self):
        import App.signals