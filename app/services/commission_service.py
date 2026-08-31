"""
Marketplace Commission Calculation Service
Computes platform revenue and seller net earnings per order item or transaction.
"""

from typing import Dict, Any


class CommissionService:
    DEFAULT_COMMISSION_RATE = 10.0  # 10%

    CATEGORY_COMMISSION_RATES = {
        "cat-electronics": 10.0,
        "cat-fashion": 12.0,
        "cat-home": 15.0,
        "cat-beauty": 8.0,
        "cat-accessories": 12.0,
    }

    def get_commission_rate(self, category_id: str, seller_custom_rate: float = None) -> float:
        if seller_custom_rate is not None and seller_custom_rate > 0:
            return float(seller_custom_rate)
        return self.CATEGORY_COMMISSION_RATES.get(category_id, self.DEFAULT_COMMISSION_RATE)

    def calculate(self, item_price: float, quantity: int, category_id: str = None, seller_custom_rate: float = None) -> Dict[str, float]:
        subtotal = float(item_price) * int(quantity)
        rate = self.get_commission_rate(category_id, seller_custom_rate)
        commission_amount = round((subtotal * rate) / 100.0, 2)
        seller_net = round(subtotal - commission_amount, 2)

        return {
            "subtotal": subtotal,
            "commission_rate": rate,
            "commission_amount": commission_amount,
            "seller_net_earning": seller_net,
        }


commission_service = CommissionService()
