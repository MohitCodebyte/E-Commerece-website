"""
Order Processing & Multi-Vendor Fulfillment Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import order_repo, product_repo, seller_repo
from app.services.commission_service import commission_service
from app.services.cart_service import cart_service


class OrderService:
    def __init__(self):
        self.repo = order_repo

    def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(order_id)

    def get_orders_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_customer(customer_id)

    def get_orders_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_seller(seller_id)

    def get_all_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repo.get_all(status=status)

    def place_order(
        self,
        customer: Dict[str, Any],
        shipping_address: Dict[str, Any],
        payment_method: str = "UPI",
    ) -> Dict[str, Any]:
        cart = cart_service.get_cart_details()
        if not cart["items"]:
            raise ValueError("Shopping cart is empty.")

        # Build order items with calculated commissions
        order_items = []
        for item in cart["items"]:
            seller = seller_repo.get_by_id(item["seller_id"])
            seller_custom_rate = seller.get("commission_rate") if seller else None

            comm = commission_service.calculate(
                item_price=item["price"],
                quantity=item["quantity"],
                category_id=item.get("category_id"),
                seller_custom_rate=seller_custom_rate,
            )

            order_items.append({
                "product_id": item["product_id"],
                "product_title": item["title"],
                "variant_name": item.get("variant_name"),
                "sku": item.get("sku"),
                "price": item["price"],
                "quantity": item["quantity"],
                "seller_id": item["seller_id"],
                "seller_name": item["seller_name"],
                "commission_rate": comm["commission_rate"],
                "commission_amount": comm["commission_amount"],
                "seller_net_earning": comm["seller_net_earning"],
                "image": item["image"],
            })

            # Update seller pending balance
            if seller:
                seller["payout_balance"] = seller.get("payout_balance", 0.0) + comm["seller_net_earning"]
                seller["lifetime_earnings"] = seller.get("lifetime_earnings", 0.0) + comm["seller_net_earning"]

        order_data = {
            "customer_id": customer.get("id", "guest"),
            "customer_name": customer.get("name", "Customer"),
            "customer_email": customer.get("email", ""),
            "customer_phone": customer.get("phone", ""),
            "shipping_address": shipping_address,
            "status": "processing",
            "payment_status": "paid",
            "payment_method": payment_method,
            "subtotal": cart["subtotal"],
            "tax": cart["tax"],
            "shipping_fee": cart["shipping_fee"],
            "discount": cart["discount"],
            "coupon_code": cart["applied_coupon"]["code"] if cart["applied_coupon"] else None,
            "total": cart["total"],
            "items": order_items,
        }

        order = self.repo.create(order_data)
        cart_service.clear_cart()
        return order

    def update_order_status(self, order_id: str, new_status: str, note: Optional[str] = None) -> Optional[Dict[str, Any]]:
        return self.repo.update_status(order_id, new_status, timeline_note=note)


order_service = OrderService()
