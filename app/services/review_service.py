"""
Customer Reviews & Ratings Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import review_repo, product_repo


class ReviewService:
    def __init__(self):
        self.repo = review_repo

    def get_product_reviews(self, product_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_product(product_id)

    def get_user_reviews(self, user_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_user(user_id)

    def get_seller_reviews(self, seller_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_seller(seller_id)

    def get_all_reviews(self) -> List[Dict[str, Any]]:
        return self.repo.get_all()

    def add_review(self, user: Dict[str, Any], product_id: str, rating: int, title: str, comment: str) -> Dict[str, Any]:
        prod = product_repo.get_by_id(product_id)
        if not prod:
            raise ValueError("Product not found.")

        review_data = {
            "product_id": product_id,
            "product_title": prod.get("title"),
            "user_id": user["id"],
            "user_name": user["name"],
            "user_avatar": user.get("avatar", ""),
            "rating": rating,
            "title": title,
            "comment": comment,
        }
        return self.repo.create(review_data)

    def reply_to_review(self, review_id: str, reply_text: str) -> bool:
        return self.repo.respond_to_review(review_id, reply_text)


review_service = ReviewService()
