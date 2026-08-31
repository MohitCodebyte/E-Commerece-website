"""
Cart & Wishlist Service
Manages shopping cart and wishlist states in Flask session.
"""

from typing import Dict, Any, List
from flask import session
from app.repositories import product_repo, coupon_repo


class CartService:
    TAX_RATE = 0.18  # 18% GST in India
    FREE_SHIPPING_THRESHOLD = 999.0
    DEFAULT_SHIPPING_FEE = 150.0

    def _get_cart(self) -> List[Dict[str, Any]]:
        if "cart" not in session:
            session["cart"] = []
        return session["cart"]

    def _get_wishlist(self) -> List[str]:
        if "wishlist" not in session:
            session["wishlist"] = []
        return session["wishlist"]

    def add_to_cart(self, product_id: str, quantity: int = 1, variant_id: str = None) -> Dict[str, Any]:
        product = product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        cart = self._get_cart()
        # Look for existing line item with same product & variant
        for item in cart:
            if item["product_id"] == product_id and item.get("variant_id") == variant_id:
                item["quantity"] += quantity
                session.modified = True
                return self.get_cart_details()

        # Find variant details if specified
        variant_name = None
        price = product["price"]
        if variant_id and "variants" in product:
            for v in product["variants"]:
                if v["id"] == variant_id:
                    variant_name = v["name"]
                    price = v.get("price", price)
                    break

        new_item = {
            "product_id": product["id"],
            "title": product["title"],
            "slug": product["slug"],
            "price": float(price),
            "image": product["thumbnail"],
            "variant_id": variant_id,
            "variant_name": variant_name,
            "quantity": quantity,
            "seller_id": product["seller_id"],
            "seller_name": product["seller_name"],
            "sku": product["sku"],
            "category_id": product["category_id"],
        }
        cart.append(new_item)
        session.modified = True
        return self.get_cart_details()

    def update_quantity(self, product_id: str, quantity: int, variant_id: str = None) -> Dict[str, Any]:
        cart = self._get_cart()
        if quantity <= 0:
            return self.remove_from_cart(product_id, variant_id)

        for item in cart:
            if item["product_id"] == product_id and item.get("variant_id") == variant_id:
                item["quantity"] = quantity
                break
        session.modified = True
        return self.get_cart_details()

    def remove_from_cart(self, product_id: str, variant_id: str = None) -> Dict[str, Any]:
        cart = self._get_cart()
        session["cart"] = [
            item for item in cart
            if not (item["product_id"] == product_id and item.get("variant_id") == variant_id)
        ]
        session.modified = True
        return self.get_cart_details()

    def clear_cart(self):
        session["cart"] = []
        session.pop("applied_coupon", None)
        session.modified = True

    def apply_coupon(self, code: str) -> Dict[str, Any]:
        coupon = coupon_repo.get_by_code(code)
        if not coupon:
            raise ValueError("Invalid coupon code or expired.")

        subtotal = sum(i["price"] * i["quantity"] for i in self._get_cart())
        if subtotal < coupon.get("min_order_amount", 0):
            raise ValueError(f"Minimum order amount of ₹{coupon['min_order_amount']:,.0f} required for this coupon.")

        session["applied_coupon"] = coupon
        session.modified = True
        return self.get_cart_details()

    def remove_coupon(self) -> Dict[str, Any]:
        session.pop("applied_coupon", None)
        session.modified = True
        return self.get_cart_details()

    def get_cart_details(self) -> Dict[str, Any]:
        cart = self._get_cart()
        subtotal = sum(i["price"] * i["quantity"] for i in cart)
        item_count = sum(i["quantity"] for i in cart)

        coupon = session.get("applied_coupon")
        discount = 0.0
        if coupon and subtotal > 0:
            if coupon["discount_type"] == "percentage":
                discount = (subtotal * coupon["discount_value"]) / 100.0
                if "max_discount" in coupon:
                    discount = min(discount, coupon["max_discount"])
            elif coupon["discount_type"] == "fixed":
                discount = min(subtotal, coupon["discount_value"])

        # Shipping logic
        if subtotal == 0 or subtotal >= self.FREE_SHIPPING_THRESHOLD:
            shipping_fee = 0.0
        else:
            shipping_fee = self.DEFAULT_SHIPPING_FEE

        # GST tax calculation
        taxable_amount = max(0.0, subtotal - discount)
        tax = round(taxable_amount * self.TAX_RATE, 2)
        total = round(taxable_amount + tax + shipping_fee, 2)

        return {
            "items": cart,
            "cart_items": cart,
            "item_count": item_count,
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "tax": tax,
            "shipping_fee": round(shipping_fee, 2),
            "total": total,
            "applied_coupon": coupon,
            "free_shipping_threshold": self.FREE_SHIPPING_THRESHOLD,
            "amount_for_free_shipping": max(0.0, self.FREE_SHIPPING_THRESHOLD - subtotal),
        }

    # Wishlist methods
    def get_wishlist_items(self) -> List[Dict[str, Any]]:
        wishlist_ids = self._get_wishlist()
        items = []
        for pid in wishlist_ids:
            prod = product_repo.get_by_id(pid)
            if prod:
                items.append(prod)
        return items

    def toggle_wishlist(self, product_id: str) -> bool:
        wishlist = self._get_wishlist()
        if product_id in wishlist:
            wishlist.remove(product_id)
            is_in_wishlist = False
        else:
            wishlist.append(product_id)
            is_in_wishlist = True
        session.modified = True
        return is_in_wishlist

    def is_in_wishlist(self, product_id: str) -> bool:
        return product_id in self._get_wishlist()


cart_service = CartService()
