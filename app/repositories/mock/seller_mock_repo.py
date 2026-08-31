"""
Seller Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from .store import mock_store
from app.repositories.base import ISellerRepository


class SellerMockRepository(ISellerRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_id(self, seller_id: str) -> Optional[Dict[str, Any]]:
        for s in self.store.sellers:
            if s["id"] == seller_id:
                return s
        return None

    def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        if not slug:
            return None
        slug_clean = slug.strip().lower()
        for s in self.store.sellers:
            if s.get("slug", "").lower() == slug_clean:
                return s
        return None

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        email_clean = email.strip().lower()
        for s in self.store.sellers:
            if s.get("email", "").lower() == email_clean:
                return s
        return None

    def get_all(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return [s for s in self.store.sellers if s.get("status") == status]
        return list(self.store.sellers)

    def create(self, seller_data: Dict[str, Any]) -> Dict[str, Any]:
        seller_id = seller_data.get("id") or f"seller-{len(self.store.sellers) + 1}"
        store_name = seller_data.get("store_name", "New Store")
        slug = seller_data.get("slug") or store_name.lower().replace(" ", "-")

        new_seller = {
            "id": seller_id,
            "store_name": store_name,
            "slug": slug,
            "legal_name": seller_data.get("legal_name", store_name),
            "email": seller_data.get("email", "").strip().lower(),
            "phone": seller_data.get("phone", ""),
            "address": seller_data.get("address", ""),
            "city": seller_data.get("city", "Mumbai"),
            "state": seller_data.get("state", "Maharashtra"),
            "pincode": seller_data.get("pincode", "400001"),
            "gstin": seller_data.get("gstin", ""),
            "pan": seller_data.get("pan", ""),
            "bank_account": seller_data.get("bank_account", {
                "account_name": store_name,
                "account_number": "000000000000",
                "ifsc": "HDFC0000001",
                "bank_name": "HDFC Bank",
                "branch": "Main Branch"
            }),
            "rating": 5.0,
            "total_reviews": 0,
            "commission_rate": float(seller_data.get("commission_rate", 10.0)),
            "status": seller_data.get("status", "pending"),
            "kyc_status": seller_data.get("kyc_status", "under_review"),
            "payout_balance": 0.0,
            "lifetime_earnings": 0.0,
            "banner": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s1200",
            "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuB2NOZ9Tw1k4m0Z5Y8n7m6l5k4j3h2g1f0d9s8a7q6w5e=s200",
            "joined_date": "2024-08-31",
        }
        self.store.sellers.append(new_seller)
        return new_seller

    def update(self, seller_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        seller = self.get_by_id(seller_id)
        if not seller:
            return None
        for k, v in updates.items():
            if k != "id":
                seller[k] = v
        return seller
