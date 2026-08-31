"""
Notification Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .store import mock_store
from app.repositories.base import INotificationRepository


class NotificationMockRepository(INotificationRepository):
    def __init__(self):
        self.store = mock_store

    def get_for_user(self, user_id: str, role: str) -> List[Dict[str, Any]]:
        results = []
        for n in self.store.notifications:
            if n.get("recipient_id") == user_id or n.get("recipient_role") == role:
                results.append(n)
        return results

    def create(self, notif_data: Dict[str, Any]) -> Dict[str, Any]:
        notif_id = f"notif-{uuid.uuid4().hex[:6]}"
        new_n = {
            "id": notif_id,
            "recipient_role": notif_data.get("recipient_role", "customer"),
            "recipient_id": notif_data.get("recipient_id"),
            "title": notif_data.get("title", "Notification"),
            "message": notif_data.get("message", ""),
            "icon": notif_data.get("icon", "notifications"),
            "type": notif_data.get("type", "info"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "is_read": False,
            "link": notif_data.get("link", "#")
        }
        self.store.notifications.insert(0, new_n)
        return new_n

    def mark_read(self, notif_id: str) -> bool:
        for n in self.store.notifications:
            if n["id"] == notif_id:
                n["is_read"] = True
                return True
        return False
