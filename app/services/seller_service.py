"""
Seller Portal Management Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import seller_repo, product_repo, order_repo


class SellerService:
    def __init__(self):
        self.repo = seller_repo

    def _enrich_seller(self, seller: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not seller:
            return None
        s = dict(seller)
        s.setdefault("balance", s.get("payout_balance", 0.0))
        s.setdefault("bank_details", s.get("bank_account", {}))
        s.setdefault("logo", s.get("avatar", ""))
        s.setdefault("contact_email", s.get("email", ""))
        s.setdefault("contact_phone", s.get("phone", ""))
        return s

    def get_seller_by_id(self, seller_id: str) -> Optional[Dict[str, Any]]:
        seller = self.repo.get_by_id(seller_id)
        return self._enrich_seller(seller)

    def get_seller_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        seller = self.repo.get_by_slug(slug)
        return self._enrich_seller(seller)

    def get_all_sellers(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        sellers = self.repo.get_all(status=status)
        return [self._enrich_seller(s) for s in sellers]

    def update_seller(self, seller_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        seller = self.repo.update(seller_id, updates)
        return self._enrich_seller(seller)

    def get_seller_metrics(self, seller_id: str) -> Dict[str, Any]:
        seller = self.get_seller_by_id(seller_id)
        if not seller:
            return {}

        products = product_repo.get_all(seller_id=seller_id)
        orders = order_repo.get_by_seller(seller_id)

        total_orders = len(orders)
        total_products = len(products)
        low_stock_count = sum(1 for p in products if p.get("stock", 0) <= p.get("low_stock_threshold", 10))

        gross_sales = sum(o.get("seller_subtotal", 0) for o in orders)
        commissions_paid = sum(o.get("seller_commission", 0) for o in orders)
        net_earnings = sum(o.get("seller_net", 0) for o in orders)

        metrics = {
            "seller": seller,
            "total_products": total_products,
            "total_orders": total_orders,
            "low_stock_count": low_stock_count,
            "gross_sales": gross_sales,
            "gmv": gross_sales,
            "commissions_paid": commissions_paid,
            "total_commission": commissions_paid,
            "net_earnings": net_earnings,
            "balance": seller.get("balance", 0.0),
            "payout_balance": seller.get("payout_balance", 0.0),
            "lifetime_earnings": seller.get("lifetime_earnings", 0.0),
            "rating": seller.get("rating", 5.0),
            "total_reviews": seller.get("total_reviews", 0),
            "recent_orders": orders[:5],
            "top_products": products[:5],
        }
        return metrics


seller_service = SellerService()
