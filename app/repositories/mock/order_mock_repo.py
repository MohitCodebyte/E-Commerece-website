"""
Order Mock Repository with Multi-Vendor Isolation
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .store import mock_store
from app.repositories.base import IOrderRepository


class OrderMockRepository(IOrderRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        for o in self.store.orders:
            if o["id"] == order_id:
                return o
        return None

    def get_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        return [o for o in self.store.orders if o.get("customer_id") == customer_id]

    def get_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        """Returns orders containing at least one item from this seller, with calculated seller earnings."""
        results = []
        for o in self.store.orders:
            seller_items = [item for item in o.get("items", []) if item.get("seller_id") == seller_id]
            if seller_items:
                # Create a view specific to this seller
                seller_subtotal = sum(i["price"] * i["quantity"] for i in seller_items)
                seller_commission = sum(i.get("commission_amount", 0) for i in seller_items)
                seller_net = sum(i.get("seller_net_earning", 0) for i in seller_items)
                
                order_view = dict(o)
                order_view["seller_items"] = seller_items
                order_view["seller_item_count"] = sum(i.get("quantity", 1) for i in seller_items)
                order_view["seller_subtotal"] = seller_subtotal
                order_view["seller_commission"] = seller_commission
                order_view["seller_net"] = seller_net
                order_view["seller_net_earning"] = seller_net
                results.append(order_view)
        return results

    def get_all(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return [o for o in self.store.orders if o.get("status") == status]
        return list(self.store.orders)

    def create(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        order_num = f"ORD-{datetime.now().year}-{len(self.store.orders) + 8901}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        new_order = {
            "id": order_num,
            "customer_id": order_data.get("customer_id", "guest"),
            "customer_name": order_data.get("customer_name", "Customer"),
            "customer_email": order_data.get("customer_email", ""),
            "customer_phone": order_data.get("customer_phone", ""),
            "shipping_address": order_data.get("shipping_address", {}),
            "order_date": now_str,
            "status": order_data.get("status", "processing"),
            "payment_status": order_data.get("payment_status", "paid"),
            "payment_method": order_data.get("payment_method", "UPI"),
            "subtotal": float(order_data.get("subtotal", 0.0)),
            "tax": float(order_data.get("tax", 0.0)),
            "shipping_fee": float(order_data.get("shipping_fee", 0.0)),
            "discount": float(order_data.get("discount", 0.0)),
            "coupon_code": order_data.get("coupon_code"),
            "total": float(order_data.get("total", 0.0)),
            "tracking_number": f"DEL-EXP-{uuid.uuid4().hex[:8].upper()}",
            "carrier": "Delhivery Express",
            "estimated_delivery": order_data.get("estimated_delivery", "3-5 Business Days"),
            "delivered_date": None,
            "tracking_timeline": [
                {"status": "Order Placed", "time": now_str, "location": "Online Store", "completed": True},
                {"status": "Payment Confirmed", "time": now_str, "location": "Secure Gateway", "completed": True},
                {"status": "Processing in Warehouse", "time": "In Progress", "location": "Fulfillment Center", "completed": True},
                {"status": "Shipped in Transit", "time": "Pending", "location": "Logistics Hub", "completed": False},
                {"status": "Delivered", "time": "Pending", "location": "Customer Address", "completed": False},
            ],
            "items": order_data.get("items", []),
            "total_commission": sum(i.get("commission_amount", 0) for i in order_data.get("items", []))
        }
        self.store.orders.insert(0, new_order)
        return new_order

    def update_status(self, order_id: str, status: str, timeline_note: Optional[str] = None) -> Optional[Dict[str, Any]]:
        order = self.get_by_id(order_id)
        if not order:
            return None
        order["status"] = status
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if status == "delivered":
            order["delivered_date"] = now_str
            order["payment_status"] = "paid"
            for step in order.get("tracking_timeline", []):
                step["completed"] = True
        elif status == "shipped":
            for step in order.get("tracking_timeline", []):
                if step["status"] in ["Order Placed", "Payment Confirmed", "Processing in Warehouse", "Shipped in Transit"]:
                    step["completed"] = True
                    if step["status"] == "Shipped in Transit":
                        step["time"] = now_str
        
        if timeline_note:
            order["tracking_timeline"].append({
                "status": f"Status Update: {status.title()}",
                "time": now_str,
                "location": timeline_note,
                "completed": True
            })
        return order
