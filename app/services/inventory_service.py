"""
Inventory Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import inventory_repo, product_repo


class InventoryService:
    def __init__(self):
        self.repo = inventory_repo

    def get_seller_logs(self, seller_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_logs_by_seller(seller_id)

    def get_all_logs(self) -> List[Dict[str, Any]]:
        return self.repo.get_all_logs()

    def adjust_stock(self, product_id: str, quantity_change: int, reason: str, adjusted_by: str) -> Optional[Dict[str, Any]]:
        return self.repo.adjust_stock(product_id, quantity_change, reason, adjusted_by)

    def get_inventory_summary(self, seller_id: Optional[str] = None) -> Dict[str, Any]:
        products = product_repo.get_all(seller_id=seller_id)
        total_items = sum(p.get("stock", 0) for p in products)
        low_stock = [p for p in products if 0 < p.get("stock", 0) <= p.get("low_stock_threshold", 10)]
        out_of_stock = [p for p in products if p.get("stock", 0) == 0]
        healthy_stock = [p for p in products if p.get("stock", 0) > p.get("low_stock_threshold", 10)]

        return {
            "products": products,
            "total_skus": len(products),
            "total_items": total_items,
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "healthy_count": len(healthy_stock),
            "low_stock_items": low_stock,
            "out_of_stock_items": out_of_stock,
        }


inventory_service = InventoryService()
