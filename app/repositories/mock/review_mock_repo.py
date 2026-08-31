"""
Review Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .store import mock_store
from app.repositories.base import IReviewRepository


class ReviewMockRepository(IReviewRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_product(self, product_id: str) -> List[Dict[str, Any]]:
        return [r for r in self.store.reviews if r.get("product_id") == product_id and r.get("status") == "approved"]

    def get_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        return [r for r in self.store.reviews if r.get("user_id") == user_id]

    def get_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        seller_prod_ids = {p["id"] for p in self.store.products if p.get("seller_id") == seller_id}
        return [r for r in self.store.reviews if r.get("product_id") in seller_prod_ids]

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.store.reviews)

    def create(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        rev_id = f"rev-{uuid.uuid4().hex[:6]}"
        new_rev = {
            "id": rev_id,
            "product_id": review_data.get("product_id"),
            "product_title": review_data.get("product_title", "Product"),
            "user_id": review_data.get("user_id"),
            "user_name": review_data.get("user_name", "Customer"),
            "user_avatar": review_data.get("user_avatar", "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s200"),
            "rating": int(review_data.get("rating", 5)),
            "title": review_data.get("title", ""),
            "comment": review_data.get("comment", ""),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "verified_purchase": True,
            "helpful_count": 0,
            "seller_response": None,
            "status": "approved"
        }
        self.store.reviews.insert(0, new_rev)
        
        # update product rating and count
        prod = next((p for p in self.store.products if p["id"] == new_rev["product_id"]), None)
        if prod:
            prod_revs = [r for r in self.store.reviews if r.get("product_id") == prod["id"]]
            prod["review_count"] = len(prod_revs)
            prod["rating"] = round(sum(r["rating"] for r in prod_revs) / len(prod_revs), 1)

        return new_rev

    def respond_to_review(self, review_id: str, response: str) -> bool:
        for r in self.store.reviews:
            if r["id"] == review_id:
                r["seller_response"] = response
                return True
        return False
