from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        """
Import signal handlers when the app is ready.
This ensures signals are connected.
        """
        try:
            import blog.signals  # noqa: F401
        except ImportError:
            # Signals module doesn't exist yet, which is fine for initial setup
            pass