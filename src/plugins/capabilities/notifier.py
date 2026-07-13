import logging
from winotify import Notification

logger = logging.getLogger(__name__)

class OSNotifier:
    def __init__(self):
        self.app_id = "AI Executive Assistant"

    def send_notification(self, title: str, msg: str, icon: str = None, actions: list = None):
        """Sends a native Windows Toast Notification with optional buttons."""
        try:
            toast = Notification(
                app_id=self.app_id,
                title=title,
                msg=msg,
                duration="short"
            )
            # You can set an absolute path to an icon file if you want
            # if icon:
            #     toast.set_icon(icon)
            
            if actions:
                for action in actions:
                    toast.add_actions(label=action["label"], launch=action["launch"])
                
            toast.show()
            logger.info(f"OS Notification sent: {title}")
        except Exception as e:
            logger.error(f"Failed to send OS Notification: {e}")

notifier = OSNotifier()
