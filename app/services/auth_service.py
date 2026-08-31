"""
Authentication & Authorization Service
Handles user login, registration, password hashing abstraction, and role checks.
"""

from typing import Optional, Dict, Any
from flask import session
from app.repositories import user_repo, seller_repo


class AuthService:
    def __init__(self):
        self.repo = user_repo

    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        if not email or not password:
            return None
        user = self.repo.get_by_email(email)
        if not user:
            return None
        # Phase 1: Simple demo matching (production ready abstraction)
        if user.get("password") == password:
            return user
        return None

    def login_user(self, user: Dict[str, Any]):
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]
        session["seller_id"] = user.get("seller_id")
        session.permanent = True

    def logout_user(self):
        session.pop("user_id", None)
        session.pop("user_name", None)
        session.pop("user_email", None)
        session.pop("user_role", None)
        session.pop("seller_id", None)

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        user_id = session.get("user_id")
        if not user_id:
            return None
        return self.repo.get_by_id(user_id)

    def register_customer(self, name: str, email: str, password: str, phone: str = "") -> Dict[str, Any]:
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email already exists.")
        
        user_data = {
            "name": name,
            "email": email,
            "password": password,
            "role": "customer",
            "phone": phone
        }
        return self.repo.create(user_data)

    def register_seller(self, store_name: str, name: str, email: str, password: str, phone: str, gstin: str = "", pan: str = "", city: str = "Mumbai", state: str = "Maharashtra") -> Dict[str, Any]:
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email already exists.")

        new_seller = seller_repo.create({
            "store_name": store_name,
            "legal_name": f"{store_name} Pvt Ltd",
            "email": email,
            "phone": phone,
            "city": city,
            "state": state,
            "gstin": gstin,
            "pan": pan,
            "status": "pending",
            "kyc_status": "under_review"
        })

        user_data = {
            "name": name,
            "email": email,
            "password": password,
            "role": "seller",
            "phone": phone,
            "seller_id": new_seller["id"]
        }
        user = self.repo.create(user_data)
        return user


auth_service = AuthService()
