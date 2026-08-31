"""
NOVA MART - Flask Application Factory
"""

import os
from flask import Flask, render_template, session
from app.config import Config


def create_app(config_class="default"):
    app = Flask(__name__)
    if isinstance(config_class, str):
        from app.config import config_by_name
        config_obj = config_by_name.get(config_class, config_by_name["default"])
    else:
        config_obj = config_class
    app.config.from_object(config_obj)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.customer import customer_bp
    from app.routes.seller import seller_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)

    # Global Context Processors for Jinja Templates
    from app.services import auth_service, cart_service, product_service, seller_service

    @app.context_processor
    def inject_global_context():
        user = auth_service.get_current_user()
        cart_info = cart_service.get_cart_details()
        wishlist_items = cart_service.get_wishlist_items()
        cats = product_service.get_categories()
        active_seller = None
        if user and user.get("seller_id"):
            active_seller = seller_service.get_seller_by_id(user["seller_id"])

        return {
            "current_user": user,
            "cart": cart_info,
            "cart_count": cart_info.get("item_count", 0),
            "wishlist_count": len(wishlist_items),
            "categories": cats,
            "platform_name": "NOVA MART",
            "active_role": user.get("role") if user else None,
            "active_seller": active_seller,
            "seller": active_seller,
        }

    # Template Filters
    @app.template_filter("currency")
    def format_currency(value):
        try:
            val = float(value)
            # Indian numbering format or standard comma separated
            return f"₹{val:,.2f}".replace(".00", "")
        except (ValueError, TypeError):
            return f"₹{value}"

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("errors/500.html"), 500

    return app
