"""
Payout Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .store import mock_store
from app.repositories.base import IPayoutRepository


class PayoutMockRepository(IPayoutRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        return [p for p in self.store.payouts if p.get("seller_id") == seller_id]

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.store.payouts)

    def create_request(self, payout_data: Dict[str, Any]) -> Dict[str, Any]:
        payout_id = f"PAY-{datetime.now().year}-{len(self.store.payouts) + 301}"
        seller_id = payout_data.get("seller_id")
        amount = float(payout_data.get("amount", 0.0))
        
        # Deduct from seller balance
        seller = next((s for s in self.store.sellers if s["id"] == seller_id), None)
        if seller:
            seller["payout_balance"] = max(0.0, seller.get("payout_balance", 0.0) - amount)

        new_payout = {
            "id": payout_id,
            "seller_id": seller_id,
            "seller_name": payout_data.get("seller_name", "Seller"),
            "amount": amount,
            "status": "processing",
            "requested_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "processed_at": None,
            "bank_account": payout_data.get("bank_account", "Bank Transfer"),
            "reference_id": f"REQ-{uuid.uuid4().hex[:8].upper()}"
        }
        self.store.payouts.insert(0, new_payout)
        return new_payout

    def update_status(self, payout_id: str, status: str) -> Optional[Dict[str, Any]]:
        for p in self.store.payouts:
            if p["id"] == payout_id:
                p["status"] = status
                if status == "completed":
                    p["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    p["reference_id"] = f"NEFT-UTR-{uuid.uuid4().hex[:10].upper()}"
                return p
        return None
