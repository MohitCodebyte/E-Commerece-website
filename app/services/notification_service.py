"""
Notification Service
"""

from typing import List, Dict, Any
from app.repositories import notification_repo


class NotificationService:
    def __init__(self):
        self.repo = notification_repo

    def get_user_notifications(self, user_id: str, role: str) -> List[Dict[str, Any]]:
        return self.repo.get_for_user(user_id, role)

    def send_notification(self, role: str, title: str, message: str, user_id: str = None, icon: str = "notifications", notif_type: str = "info", link: str = "#") -> Dict[str, Any]:
        return self.repo.create({
            "recipient_role": role,
            "recipient_id": user_id,
            "title": title,
            "message": message,
            "icon": icon,
            "type": notif_type,
            "link": link,
        })

    def mark_as_read(self, notif_id: str) -> bool:
        return self.repo.mark_read(notif_id)


notification_service = NotificationService()
