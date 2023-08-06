
from django.apps import AppConfig


class AgileTixAppConfig(AppConfig):

    name = 'agiletix'
    verbose_name = 'Agile Ticketing App'

    def ready(self):

        # This code was borrowed from django.contrib.admin 
        # We use the same registry strategy for the sync service.

        # autodiscover
        import imp
        from importlib import import_module
        from django.conf import settings

        for app in settings.INSTALLED_APPS:
            # For each app, we need to look for an agile_sync.py inside that app's package. 

            # Step 1: find out the app's __path__
            try:
                app_path = import_module(app).__path__
            except AttributeError:
                continue

            # Step 2: use imp.find_module to find the app's agile_sync.py.
            try:
                imp.find_module('agile_sync', app_path)
            except ImportError:
                continue

            # Step 3: import the app's agile_sync file. 
            import_module("%s.agile_sync" % app)

