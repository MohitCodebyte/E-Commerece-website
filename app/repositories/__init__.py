"""
Repositories Module
In Phase 1, instantiate and expose mock repositories.
In Phase 2, a factory or configuration switch will return database repositories
matching the exact same Base interfaces.
"""

from .mock.user_mock_repo import UserMockRepository
from .mock.product_mock_repo import ProductMockRepository
from .mock.order_mock_repo import OrderMockRepository
from .mock.seller_mock_repo import SellerMockRepository
from .mock.category_mock_repo import CategoryMockRepository
from .mock.coupon_mock_repo import CouponMockRepository
from .mock.notification_mock_repo import NotificationMockRepository
from .mock.review_mock_repo import ReviewMockRepository
from .mock.inventory_mock_repo import InventoryMockRepository
from .mock.payout_mock_repo import PayoutMockRepository

user_repo = UserMockRepository()
product_repo = ProductMockRepository()
order_repo = OrderMockRepository()
seller_repo = SellerMockRepository()
category_repo = CategoryMockRepository()
coupon_repo = CouponMockRepository()
notification_repo = NotificationMockRepository()
review_repo = ReviewMockRepository()
inventory_repo = InventoryMockRepository()
payout_repo = PayoutMockRepository()

__all__ = [
    "user_repo",
    "product_repo",
    "order_repo",
    "seller_repo",
    "category_repo",
    "coupon_repo",
    "notification_repo",
    "review_repo",
    "inventory_repo",
    "payout_repo",
]
