"""
Super Admin Portal Routes (/admin)
Global administrative control over marketplace, all sellers, products, orders, and commissions.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services import (
    product_service,
    order_service,
    seller_service,
    inventory_service,
    payout_service,
    review_service,
    notification_service,
    auth_service,
)
from app.repositories import user_repo, category_repo, coupon_repo
from app.repositories.mock.store import mock_store
from app.utils.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    all_orders = order_service.get_all_orders()
    all_products = product_service.list_products()
    all_sellers = seller_service.get_all_sellers()
    all_customers = user_repo.get_all(role="customer")

    total_gmv = sum(o.get("total", 0) for o in all_orders)
    total_commission = sum(
        sum(item.get("commission_amount", 0) for item in o.get("items", []))
        for o in all_orders
    )

    metrics = {
        "total_gmv": total_gmv,
        "total_commission": total_commission,
        "total_orders": len(all_orders),
        "total_products": len(all_products),
        "total_sellers": len(all_sellers),
        "total_customers": len(all_customers),
    }
    recent_orders = all_orders[:6]
    top_sellers = all_sellers[:4]

    return render_template(
        "admin/dashboard.html",
        metrics=metrics,
        recent_orders=recent_orders,
        sellers=top_sellers,
        **metrics
    )


@admin_bp.route("/analytics")
@role_required("admin")
def analytics():
    all_orders = order_service.get_all_orders()
    all_sellers = seller_service.get_all_sellers()
    total_gmv = sum(o.get("total", 0) for o in all_orders)
    total_commission = sum(
        sum(item.get("commission_amount", 0) for item in o.get("items", []))
        for o in all_orders
    )
    return render_template(
        "admin/analytics.html",
        total_gmv=total_gmv,
        total_commission=total_commission,
        orders=all_orders,
        sellers=all_sellers,
    )


# --- PRODUCT CATALOG MANAGEMENT ---

@admin_bp.route("/products")
@role_required("admin")
def products():
    all_prods = product_service.list_products()
    sellers = seller_service.get_all_sellers()
    categories = product_service.get_categories()
    return render_template("admin/products.html", products=all_prods, sellers=sellers, categories=categories)


@admin_bp.route("/products/add", methods=["GET", "POST"])
@role_required("admin")
def product_add():
    categories = product_service.get_categories()
    brands = product_service.get_brands()
    sellers = seller_service.get_all_sellers()

    if request.method == "POST":
        title = request.form.get("title")
        seller_id = request.form.get("seller_id", "seller-1")
        category_id = request.form.get("category_id")
        brand_id = request.form.get("brand_id")
        price = float(request.form.get("price", 0))
        compare_at = float(request.form.get("compare_at_price", price))
        stock = int(request.form.get("stock", 10))
        sku = request.form.get("sku")
        summary = request.form.get("summary")
        description = request.form.get("description")
        thumbnail = request.form.get("thumbnail") or "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800"

        prod = product_service.create_product({
            "title": title,
            "seller_id": seller_id,
            "category_id": category_id,
            "brand_id": brand_id,
            "price": price,
            "compare_at_price": compare_at,
            "stock": stock,
            "sku": sku,
            "summary": summary,
            "description": description,
            "thumbnail": thumbnail,
        })
        flash(f"Product '{prod['title']}' created by Admin.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_add.html", categories=categories, brands=brands, sellers=sellers)


@admin_bp.route("/products/edit/<product_id>", methods=["GET", "POST"])
@role_required("admin")
def product_edit(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        abort(404)

    categories = product_service.get_categories()
    brands = product_service.get_brands()
    sellers = seller_service.get_all_sellers()

    if request.method == "POST":
        updates = {
            "title": request.form.get("title", product["title"]),
            "price": float(request.form.get("price", product["price"])),
            "compare_at_price": float(request.form.get("compare_at_price", product.get("compare_at_price", product["price"]))),
            "stock": int(request.form.get("stock", product.get("stock", 0))),
            "summary": request.form.get("summary", product.get("summary", "")),
            "description": request.form.get("description", product.get("description", "")),
            "is_featured": "is_featured" in request.form,
            "is_active": "is_active" in request.form,
        }
        product_service.update_product(product_id, updates)
        flash("Product updated by Admin.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_edit.html", product=product, categories=categories, brands=brands, sellers=sellers)


@admin_bp.route("/products/delete/<product_id>", methods=["POST"])
@role_required("admin")
def product_delete(product_id):
    product_service.delete_product(product_id)
    flash("Product deleted from platform.", "info")
    return redirect(url_for("admin.products"))


# --- CATEGORIES & BRANDS ---

@admin_bp.route("/categories", methods=["GET", "POST"])
@role_required("admin")
def categories():
    if request.method == "POST":
        name = request.form.get("name")
        icon = request.form.get("icon", "category")
        desc = request.form.get("description", "")
        product_service.create_category({"name": name, "icon": icon, "description": desc})
        flash(f"Category '{name}' created successfully.", "success")
        return redirect(url_for("admin.categories"))

    all_cats = category_repo.get_all()
    all_brands = category_repo.get_brands()
    return render_template("admin/categories.html", categories=all_cats, brands=all_brands)


@admin_bp.route("/categories/add", methods=["POST"])
@role_required("admin")
def category_add():
    name = request.form.get("name")
    icon = request.form.get("icon", "category")
    desc = request.form.get("description", "")
    product_service.create_category({"name": name, "icon": icon, "description": desc})
    flash(f"Category '{name}' created successfully.", "success")
    return redirect(url_for("admin.categories"))


# --- GLOBAL ORDERS ---

@admin_bp.route("/orders")
@role_required("admin")
def orders():
    all_orders = order_service.get_all_orders()
    return render_template("admin/orders.html", orders=all_orders)


@admin_bp.route("/orders/<order_id>")
@role_required("admin")
def order_detail(order_id):
    order = order_service.get_order_by_id(order_id)
    if not order:
        abort(404)
    return render_template("admin/order_detail.html", order=order)


@admin_bp.route("/orders/<order_id>/update-status", methods=["POST"])
@role_required("admin")
def order_update_status(order_id):
    new_status = request.form.get("status")
    order_service.update_order_status(order_id, new_status, note="Updated by Super Admin")
    flash(f"Order #{order_id} status updated to {new_status.title()}.", "success")
    return redirect(url_for("admin.order_detail", order_id=order_id))


# --- CUSTOMERS & SELLERS ---

@admin_bp.route("/customers")
@role_required("admin")
def customers():
    all_customers = user_repo.get_all(role="customer")
    all_sellers = seller_service.get_all_sellers()
    return render_template("admin/customers.html", customers=all_customers, sellers=all_sellers)


@admin_bp.route("/customers/<customer_id>")
@role_required("admin")
def customer_detail(customer_id):
    customer = user_repo.get_by_id(customer_id)
    if not customer:
        abort(404)
    customer_orders = order_service.get_orders_by_customer(customer_id)
    return render_template("admin/customer_detail.html", customer=customer, orders=customer_orders)


# --- INVENTORY & COUPONS ---

@admin_bp.route("/inventory")
@role_required("admin")
def inventory():
    inv_data = inventory_service.get_inventory_summary()
    logs = inventory_service.get_all_logs()
    return render_template("admin/inventory.html", logs=logs, **inv_data)


@admin_bp.route("/coupons", methods=["GET", "POST"])
@role_required("admin")
def coupons():
    if request.method == "POST":
        code = request.form.get("code", "").upper().strip()
        discount_type = request.form.get("discount_type", "percentage")
        discount_value = float(request.form.get("discount_value", 10.0))
        max_discount = float(request.form.get("max_discount", 1000.0))
        min_order_amount = float(request.form.get("min_order_amount", 999.0))
        description = request.form.get("description", "")

        coupon_repo.create({
            "code": code,
            "discount_type": discount_type,
            "discount_value": discount_value,
            "max_discount": max_discount,
            "min_order_amount": min_order_amount,
            "description": description,
        })
        flash(f"Coupon '{code}' created.", "success")
        return redirect(url_for("admin.coupons"))

    all_coupons = coupon_repo.get_all()
    return render_template("admin/coupons.html", coupons=all_coupons)


@admin_bp.route("/coupons/add", methods=["POST"])
@role_required("admin")
def coupon_add():
    code = request.form.get("code", "").upper().strip()
    discount_type = request.form.get("discount_type", "percentage")
    discount_value = float(request.form.get("discount_value", 10.0))
    min_order_amount = float(request.form.get("min_order_amount", 999.0))
    coupon_repo.create({
        "code": code,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "min_order_amount": min_order_amount,
    })
    flash(f"Coupon '{code}' created.", "success")
    return redirect(url_for("admin.coupons"))


# --- REVIEWS MODERATION ---

@admin_bp.route("/reviews")
@role_required("admin")
def reviews():
    all_reviews = review_service.get_all_reviews()
    return render_template("admin/reviews.html", reviews=all_reviews)


@admin_bp.route("/reviews/delete/<review_id>", methods=["POST"])
@role_required("admin")
def review_delete(review_id):
    review_service.delete_review(review_id)
    flash("Review removed by platform moderator.", "info")
    return redirect(url_for("admin.reviews"))


# --- NOTIFICATIONS & SETTINGS ---

@admin_bp.route("/notifications", methods=["GET", "POST"])
@role_required("admin")
def notifications():
    user = auth_service.get_current_user()
    user_id = user["id"] if user else "user-admin-1"

    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        recipient_role = request.form.get("target_role") or request.form.get("recipient_role", "all")

        notification_service.send_notification(
            role=recipient_role,
            title=title,
            message=message,
            notif_type="info",
            icon="campaign"
        )
        flash("Broadcast notification dispatched.", "success")
        return redirect(url_for("admin.notifications"))

    admin_notifs = notification_service.get_user_notifications(user_id, "admin")
    return render_template("admin/notifications.html", notifications=admin_notifs)


@admin_bp.route("/notifications/broadcast", methods=["POST"])
@role_required("admin")
def broadcast():
    title = request.form.get("title")
    message = request.form.get("message")
    recipient_role = request.form.get("target_role") or request.form.get("recipient_role", "all")

    notification_service.send_notification(
        role=recipient_role,
        title=title,
        message=message,
        notif_type="info",
        icon="campaign"
    )
    flash("Broadcast notification dispatched.", "success")
    return redirect(url_for("admin.notifications"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@role_required("admin")
def settings():
    if request.method == "POST":
        flash("Platform settings saved.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html")
