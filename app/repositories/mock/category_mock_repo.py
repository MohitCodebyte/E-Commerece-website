"""
Category & Brand Mock Repository
"""

from typing import List, Optional, Dict, Any
from .store import mock_store
from app.repositories.base import ICategoryRepository


class CategoryMockRepository(ICategoryRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_id(self, cat_id: str) -> Optional[Dict[str, Any]]:
        for c in self.store.categories:
            if c["id"] == cat_id:
                return c
        return None

    def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        if not slug:
            return None
        slug_clean = slug.strip().lower()
        for c in self.store.categories:
            if c["slug"].lower() == slug_clean:
                return c
        return None

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.store.categories)

    def create(self, cat_data: Dict[str, Any]) -> Dict[str, Any]:
        cat_id = cat_data.get("id") or f"cat-{cat_data.get('slug', 'new')}"
        new_cat = {
            "id": cat_id,
            "name": cat_data.get("name", "New Category"),
            "slug": cat_data.get("slug", cat_data.get("name", "").lower().replace(" ", "-")),
            "icon": cat_data.get("icon", "category"),
            "description": cat_data.get("description", ""),
            "image": cat_data.get("image", "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800"),
            "product_count": 0,
            "is_featured": cat_data.get("is_featured", False)
        }
        self.store.categories.append(new_cat)
        return new_cat

    def get_brands(self) -> List[Dict[str, Any]]:
        return list(self.store.brands)

    def create_brand(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        brand_id = brand_data.get("id") or f"brand-{brand_data.get('slug', 'new')}"
        new_brand = {
            "id": brand_id,
            "name": brand_data.get("name", "New Brand"),
            "slug": brand_data.get("slug", brand_data.get("name", "").lower().replace(" ", "-")),
            "logo": brand_data.get("logo", "sell"),
            "is_verified": brand_data.get("is_verified", True)
        }
        self.store.brands.append(new_brand)
        return new_brand
