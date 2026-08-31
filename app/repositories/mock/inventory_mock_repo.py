"""
Inventory Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .store import mock_store
from app.repositories.base import IInventoryRepository


class InventoryMockRepository(IInventoryRepository):
    def __init__(self):
        self.store = mock_store

    def get_logs_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        return [log for log in self.store.inventory_logs if log.get("seller_id") == seller_id]

    def get_all_logs(self) -> List[Dict[str, Any]]:
        return list(self.store.inventory_logs)

    def adjust_stock(self, product_id: str, quantity_change: int, reason: str, adjusted_by: str) -> Optional[Dict[str, Any]]:
        prod = next((p for p in self.store.products if p["id"] == product_id), None)
        if not prod:
            return None
        
        prev_stock = prod.get("stock", 0)
        new_stock = max(0, prev_stock + quantity_change)
        prod["stock"] = new_stock
        
        log_id = f"inv-log-{uuid.uuid4().hex[:6]}"
        new_log = {
            "id": log_id,
            "product_id": product_id,
            "product_title": prod.get("title"),
            "sku": prod.get("sku"),
            "seller_id": prod.get("seller_id"),
            "type": "adjustment" if quantity_change >= 0 else "reduction",
            "quantity_change": quantity_change,
            "previous_stock": prev_stock,
            "new_stock": new_stock,
            "reason": reason,
            "adjusted_by": adjusted_by,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.store.inventory_logs.insert(0, new_log)
        return prod
