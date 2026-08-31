"""
Product Catalog Service
"""

from typing import List, Optional, Dict, Any
from app.repositories import product_repo, category_repo, seller_repo


class ProductService:
    def __init__(self):
        self.repo = product_repo

    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(product_id)

    def get_product_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_slug(slug)

    def list_products(
        self,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        seller_id: Optional[str] = None,
        query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: Optional[str] = None,
        is_featured: Optional[bool] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return self.repo.get_all(
            category_slug=category,
            brand_slug=brand,
            seller_id=seller_id,
            query=query,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            is_featured=is_featured,
            limit=limit,
        )

    def get_featured_products(self, limit: int = 4) -> List[Dict[str, Any]]:
        return self.repo.get_all(is_featured=True, limit=limit)

    def get_products_by_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_all(seller_id=seller_id)

    def get_categories(self) -> List[Dict[str, Any]]:
        return category_repo.get_all()

    def get_category_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        return category_repo.get_by_slug(slug)

    def create_category(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return category_repo.create(data)

    def get_brands(self) -> List[Dict[str, Any]]:
        return category_repo.get_brands()

    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Associate category and seller names
        cat = category_repo.get_by_id(data.get("category_id", ""))
        if cat:
            data["category_name"] = cat["name"]
        
        seller = seller_repo.get_by_id(data.get("seller_id", ""))
        if seller:
            data["seller_name"] = seller["store_name"]

        return self.repo.create(data)

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.repo.update(product_id, updates)

    def delete_product(self, product_id: str) -> bool:
        return self.repo.delete(product_id)


product_service = ProductService()
