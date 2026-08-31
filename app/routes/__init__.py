from .auth import auth_bp
from .customer import customer_bp
from .seller import seller_bp
from .admin import admin_bp

__all__ = ["auth_bp", "customer_bp", "seller_bp", "admin_bp"]
