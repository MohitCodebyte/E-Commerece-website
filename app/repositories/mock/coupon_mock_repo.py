"""
Coupon Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from .store import mock_store
from app.repositories.base import ICouponRepository


class CouponMockRepository(ICouponRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        if not code:
            return None
        clean_code = code.strip().upper()
        for c in self.store.coupons:
            if c["code"].upper() == clean_code and c.get("is_active"):
                return c
        return None

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.store.coupons)

    def create(self, coupon_data: Dict[str, Any]) -> Dict[str, Any]:
        cpn_id = coupon_data.get("id") or f"cpn-{uuid.uuid4().hex[:6]}"
        new_coupon = {
            "id": cpn_id,
            "code": coupon_data.get("code", "").strip().upper(),
            "discount_type": coupon_data.get("discount_type", "percentage"),
            "discount_value": float(coupon_data.get("discount_value", 10.0)),
            "max_discount": float(coupon_data.get("max_discount", 1000.0)),
            "min_order_amount": float(coupon_data.get("min_order_amount", 999.0)),
            "expires_at": coupon_data.get("expires_at", "2026-12-31"),
            "is_active": coupon_data.get("is_active", True),
            "usage_count": 0,
            "description": coupon_data.get("description", "")
        }
        self.store.coupons.append(new_coupon)
        return new_coupon
