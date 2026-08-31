"""
Thread-safe In-Memory Mock Store for Phase 1.
Provides stateful operations across sessions without requiring a database.
"""

from threading import Lock
from typing import Dict, Any, List
from app.data.mock_data import get_mock_db

class MockDataStore:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MockDataStore, cls).__new__(cls)
                cls._instance._init_data()
            return cls._instance

    def _init_data(self):
        self._data = get_mock_db()
        for o in self._data.get("orders", []):
            if "total_commission" not in o:
                o["total_commission"] = sum(i.get("commission_amount", 0) for i in o.get("items", []))
            if "items_list" not in o:
                o["items_list"] = o.get("items", [])

    def reset(self):
        with self._lock:
            self._init_data()

    @property
    def users(self) -> List[Dict[str, Any]]:
        return self._data["users"]

    @property
    def products(self) -> List[Dict[str, Any]]:
        return self._data["products"]

    @property
    def categories(self) -> List[Dict[str, Any]]:
        return self._data["categories"]

    @property
    def brands(self) -> List[Dict[str, Any]]:
        return self._data["brands"]

    @property
    def sellers(self) -> List[Dict[str, Any]]:
        return self._data["sellers"]

    @property
    def orders(self) -> List[Dict[str, Any]]:
        return self._data["orders"]

    @property
    def coupons(self) -> List[Dict[str, Any]]:
        return self._data["coupons"]

    @property
    def reviews(self) -> List[Dict[str, Any]]:
        return self._data["reviews"]

    @property
    def notifications(self) -> List[Dict[str, Any]]:
        return self._data["notifications"]

    @property
    def payouts(self) -> List[Dict[str, Any]]:
        return self._data["payouts"]

    @property
    def inventory_logs(self) -> List[Dict[str, Any]]:
        return self._data["inventory_logs"]

    @property
    def returns(self) -> List[Dict[str, Any]]:
        return self._data["returns"]

    @property
    def support_tickets(self) -> List[Dict[str, Any]]:
        return self._data["support_tickets"]


mock_store = MockDataStore()
