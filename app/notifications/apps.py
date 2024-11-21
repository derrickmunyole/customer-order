from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        try:
            import notifications.signals  # noqa: F401
            logger.debug("Notifications signals registered successfully")
        except Exception as e:
            logger.debug(f"Error registering signals: {str(e)}")
