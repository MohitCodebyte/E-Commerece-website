"""
Product Mock Repository
"""

from typing import List, Optional, Dict, Any
import uuid
import re
from .store import mock_store
from app.repositories.base import IProductRepository


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)


class ProductMockRepository(IProductRepository):
    def __init__(self):
        self.store = mock_store

    def get_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        if not product_id:
            return None
        norm_id = product_id.replace("-00", "-").replace("-0", "-")
        for p in self.store.products:
            p_norm = p["id"].replace("-00", "-").replace("-0", "-")
            if p["id"] == product_id or p_norm == norm_id:
                return p
        return None

    def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        if not slug:
            return None
        slug_clean = slug.strip().lower()
        for p in self.store.products:
            if p.get("slug", "").lower() == slug_clean:
                return p
        return None

    def get_all(
        self,
        category_slug: Optional[str] = None,
        brand_slug: Optional[str] = None,
        seller_id: Optional[str] = None,
        query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: Optional[str] = None,
        is_featured: Optional[bool] = None,
        is_active: Optional[bool] = True,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        results = list(self.store.products)

        if is_active is not None:
            results = [p for p in results if p.get("is_active") == is_active]

        if category_slug:
            # Match category slug or id
            cat = next((c for c in self.store.categories if c["slug"] == category_slug or c["id"] == category_slug), None)
            if cat:
                results = [p for p in results if p.get("category_id") == cat["id"] or p.get("category_name").lower() == cat["name"].lower()]

        if brand_slug:
            brand = next((b for b in self.store.brands if b["slug"] == brand_slug or b["id"] == brand_slug), None)
            if brand:
                results = [p for p in results if p.get("brand_id") == brand["id"] or p.get("brand_name").lower() == brand["name"].lower()]

        if seller_id:
            results = [p for p in results if p.get("seller_id") == seller_id]

        if query:
            q = query.strip().lower()
            results = [
                p for p in results
                if q in p.get("title", "").lower()
                or q in p.get("summary", "").lower()
                or q in p.get("category_name", "").lower()
                or q in p.get("brand_name", "").lower()
                or q in p.get("sku", "").lower()
            ]

        if min_price is not None:
            results = [p for p in results if p.get("price", 0) >= min_price]

        if max_price is not None:
            results = [p for p in results if p.get("price", 0) <= max_price]

        if is_featured is not None:
            results = [p for p in results if p.get("is_featured") == is_featured]

        if sort_by:
            if sort_by == "price-asc":
                results = sorted(results, key=lambda p: p.get("price", 0))
            elif sort_by == "price-desc":
                results = sorted(results, key=lambda p: p.get("price", 0), reverse=True)
            elif sort_by == "rating":
                results = sorted(results, key=lambda p: p.get("rating", 0), reverse=True)
            elif sort_by == "newest":
                results = sorted(results, key=lambda p: p.get("id", ""), reverse=True)
            elif sort_by == "popular":
                results = sorted(results, key=lambda p: p.get("review_count", 0), reverse=True)

        if limit and limit > 0:
            results = results[:limit]

        return results

    def create(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        prod_id = product_data.get("id") or f"prod-{uuid.uuid4().hex[:6]}"
        title = product_data.get("title", "Untitled Product")
        slug = product_data.get("slug") or _slugify(title)
        
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while any(p.get("slug") == slug for p in self.store.products):
            slug = f"{base_slug}-{counter}"
            counter += 1

        price = float(product_data.get("price", 0.0))
        compare_at = float(product_data.get("compare_at_price", price))
        discount = int(round(((compare_at - price) / compare_at * 100))) if compare_at > price else 0

        new_prod = {
            "id": prod_id,
            "title": title,
            "slug": slug,
            "sku": product_data.get("sku", f"NM-SKU-{uuid.uuid4().hex[:4].upper()}"),
            "category_id": product_data.get("category_id", "cat-electronics"),
            "category_name": product_data.get("category_name", "Electronics"),
            "brand_id": product_data.get("brand_id", "brand-novatech"),
            "brand_name": product_data.get("brand_name", "NovaTech"),
            "seller_id": product_data.get("seller_id", "seller-1"),
            "seller_name": product_data.get("seller_name", "TechZone Electronics"),
            "price": price,
            "compare_at_price": compare_at,
            "cost_price": float(product_data.get("cost_price", price * 0.7)),
            "discount_percent": discount,
            "stock": int(product_data.get("stock", 0)),
            "reserved_stock": 0,
            "low_stock_threshold": int(product_data.get("low_stock_threshold", 10)),
            "rating": 5.0,
            "review_count": 0,
            "badge": product_data.get("badge", "New"),
            "is_featured": product_data.get("is_featured", False),
            "is_active": product_data.get("is_active", True),
            "thumbnail": product_data.get("thumbnail") or "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800",
            "images": product_data.get("images") or [product_data.get("thumbnail") or "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800"],
            "summary": product_data.get("summary", ""),
            "description": product_data.get("description", ""),
            "features": product_data.get("features", []),
            "specifications": product_data.get("specifications", {}),
            "variants": product_data.get("variants", [])
        }
        self.store.products.append(new_prod)
        return new_prod

    def update(self, product_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        prod = self.get_by_id(product_id)
        if not prod:
            return None
        for k, v in updates.items():
            if k != "id":
                prod[k] = v
        # recalculate discount if price changed
        if "price" in updates or "compare_at_price" in updates:
            p = float(prod.get("price", 0))
            cap = float(prod.get("compare_at_price", p))
            prod["discount_percent"] = int(round(((cap - p) / cap * 100))) if cap > p else 0
        return prod

    def delete(self, product_id: str) -> bool:
        prod = self.get_by_id(product_id)
        if prod:
            self.store.products.remove(prod)
            return True
        return False
