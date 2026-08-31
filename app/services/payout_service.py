"""
Seller Payout & Withdrawals Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import payout_repo, seller_repo


class PayoutService:
    def __init__(self):
        self.repo = payout_repo

    def get_seller_payouts(self, seller_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_seller(seller_id)

    def get_all_payouts(self) -> List[Dict[str, Any]]:
        return self.repo.get_all()

    def request_payout(self, seller_id: str, amount: float, bank_account_label: str) -> Dict[str, Any]:
        seller = seller_repo.get_by_id(seller_id)
        if not seller:
            raise ValueError("Seller account not found.")

        current_balance = seller.get("payout_balance", 0.0)
        if amount <= 0:
            raise ValueError("Requested amount must be greater than zero.")
        if amount > current_balance:
            raise ValueError(f"Insufficient funds. Maximum withdrawable amount is ₹{current_balance:,.2f}.")

        payout_data = {
            "seller_id": seller_id,
            "seller_name": seller.get("store_name"),
            "amount": amount,
            "bank_account": bank_account_label,
        }
        return self.repo.create_request(payout_data)

    def process_payout(self, payout_id: str, status: str) -> Optional[Dict[str, Any]]:
        return self.repo.update_status(payout_id, status)


payout_service = PayoutService()
