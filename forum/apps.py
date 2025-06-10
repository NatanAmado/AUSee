from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'

    def ready(self):
        try:
            import forum.templatetags.forum_extras  # noqa
        except ImportError:
            pass
