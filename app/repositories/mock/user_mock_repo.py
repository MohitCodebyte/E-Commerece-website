"""
User Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from .store import mock_store
from app.repositories.base import IUserRepository


class UserMockRepository(IUserRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if not user_id:
            return None
        norm_id = user_id.replace("-00", "-").replace("-0", "-")
        for u in self.store.users:
            u_norm = u["id"].replace("-00", "-").replace("-0", "-")
            if u["id"] == user_id or u_norm == norm_id:
                return u
        return None

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        email_clean = email.strip().lower()
        for u in self.store.users:
            if u["email"].lower() == email_clean:
                return u
        return None

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = user_data.get("id") or f"user-{uuid.uuid4().hex[:8]}"
        new_user = {
            "id": user_id,
            "name": user_data.get("name", "New User"),
            "email": user_data.get("email", "").strip().lower(),
            "password": user_data.get("password", ""),
            "role": user_data.get("role", "customer"),
            "phone": user_data.get("phone", ""),
            "avatar": user_data.get("avatar", "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s200"),
            "seller_id": user_data.get("seller_id"),
            "status": "active",
            "created_at": "2024-08-31",
            "addresses": user_data.get("addresses", [])
        }
        self.store.users.append(new_user)
        return new_user

    def update(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        for k, v in updates.items():
            if k != "id":
                user[k] = v
        return user

    def get_all(self, role: Optional[str] = None) -> List[Dict[str, Any]]:
        if role:
            return [u for u in self.store.users if u.get("role") == role]
        return list(self.store.users)

    def add_address(self, user_id: str, address_data: Dict[str, Any]) -> Dict[str, Any]:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if "addresses" not in user:
            user["addresses"] = []
        
        addr_id = f"addr-{uuid.uuid4().hex[:6]}"
        is_default = address_data.get("is_default", len(user["addresses"]) == 0)
        
        if is_default:
            for a in user["addresses"]:
                a["is_default"] = False

        new_addr = {
            "id": addr_id,
            "label": address_data.get("label", "Home"),
            "recipient": address_data.get("recipient", user["name"]),
            "phone": address_data.get("phone", user.get("phone", "")),
            "street": address_data.get("street", ""),
            "city": address_data.get("city", ""),
            "state": address_data.get("state", ""),
            "pincode": address_data.get("pincode", ""),
            "is_default": is_default
        }
        user["addresses"].append(new_addr)
        return new_addr

    def get_addresses(self, user_id: str) -> List[Dict[str, Any]]:
        user = self.get_by_id(user_id)
        if not user:
            return []
        return user.get("addresses", [])
