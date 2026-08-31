"""
Seller Portal Routes (/seller)
Enforces multi-vendor isolation: A seller only accesses and manages their own store data.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.services import (
    auth_service,
    product_service,
    order_service,
    seller_service,
    inventory_service,
    payout_service,
    review_service,
    notification_service,
)
from app.repositories import seller_repo, product_repo, order_repo
from app.repositories.mock.store import mock_store
from app.utils.decorators import role_required

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")


def _get_current_seller_id():
    """Helper to retrieve active seller ID from session or default to seller-1 for demo ease."""
    seller_id = session.get("seller_id")
    if not seller_id:
        seller_id = "seller-1"
    return seller_id


# --- SELLER AUTH & ONBOARDING ---

@seller_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = auth_service.authenticate(email, password)
        if user and user.get("role") in ["seller", "admin"]:
            auth_service.login_user(user)
            flash(f"Welcome back to VendorCenter, {user['name']}!", "success")
            return redirect(url_for("seller.dashboard"))
        else:
            flash("Invalid vendor credentials. Try seller@techzone.in / seller123", "error")

    return render_template("seller/login.html")


@seller_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        store_name = request.form.get("store_name", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()
        gstin = request.form.get("gstin", "").strip()
        pan = request.form.get("pan", "").strip()

        try:
            user = auth_service.register_seller(
                store_name=store_name,
                name=name,
                email=email,
                password=password,
                phone=phone,
                gstin=gstin,
                pan=pan,
            )
            auth_service.login_user(user)
            flash("Vendor application submitted! Please complete KYC verification.", "success")
            return redirect(url_for("seller.kyc"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("seller/register.html")


@seller_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        flash(f"Vendor password recovery link dispatched to {email} (Demo).", "info")
        return redirect(url_for("seller.login"))
    return render_template("seller/forgot_password.html")


@seller_bp.route("/kyc", methods=["GET", "POST"])
@role_required("seller", "admin")
def kyc():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)

    if request.method == "POST":
        updates = {
            "gstin": request.form.get("gstin", seller.get("gstin", "")),
            "pan": request.form.get("pan", seller.get("pan", "")),
            "kyc_status": "verified",  # Auto-verify in demo
            "status": "active",
        }
        seller_service.update_seller(seller_id, updates)
        flash("KYC details submitted and verified successfully!", "success")
        return redirect(url_for("seller.application_status"))

    return render_template("seller/kyc.html", seller=seller)


@seller_bp.route("/application-status")
@role_required("seller", "admin")
def application_status():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)
    return render_template("seller/application_status.html", seller=seller)


# --- SELLER DASHBOARD & ANALYTICS ---

@seller_bp.route("/dashboard")
@role_required("seller", "admin")
def dashboard():
    seller_id = _get_current_seller_id()
    metrics = seller_service.get_seller_metrics(seller_id)
    notifications = notification_service.get_user_notifications(seller_id, "seller")
    return render_template("seller/dashboard.html", metrics=metrics, notifications=notifications, **metrics)


@seller_bp.route("/analytics")
@role_required("seller", "admin")
def analytics():
    seller_id = _get_current_seller_id()
    metrics = seller_service.get_seller_metrics(seller_id)
    return render_template("seller/analytics.html", **metrics)


@seller_bp.route("/performance")
@role_required("seller", "admin")
def performance():
    seller_id = _get_current_seller_id()
    metrics = seller_service.get_seller_metrics(seller_id)
    return render_template("seller/performance.html", **metrics)


# --- PRODUCT MANAGEMENT ---

@seller_bp.route("/products")
@role_required("seller", "admin")
def products():
    seller_id = _get_current_seller_id()
    seller_products = product_service.list_products(seller_id=seller_id)
    return render_template("seller/products.html", products=seller_products)


@seller_bp.route("/products/add", methods=["GET", "POST"])
@role_required("seller", "admin")
def product_add():
    seller_id = _get_current_seller_id()
    categories = product_service.get_categories()
    brands = product_service.get_brands()

    if request.method == "POST":
        title = request.form.get("title")
        category_id = request.form.get("category_id")
        brand_id = request.form.get("brand_id")
        price = float(request.form.get("price", 0))
        compare_at = float(request.form.get("compare_at_price", price))
        stock = int(request.form.get("stock", 10))
        sku = request.form.get("sku")
        summary = request.form.get("summary")
        description = request.form.get("description")
        thumbnail = request.form.get("thumbnail") or "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800"

        new_prod = product_service.create_product({
            "title": title,
            "category_id": category_id,
            "brand_id": brand_id,
            "seller_id": seller_id,
            "price": price,
            "compare_at_price": compare_at,
            "stock": stock,
            "sku": sku,
            "summary": summary,
            "description": description,
            "thumbnail": thumbnail,
        })
        flash(f"Product '{new_prod['title']}' created successfully!", "success")
        return redirect(url_for("seller.products"))

    return render_template("seller/product_add.html", categories=categories, brands=brands)


@seller_bp.route("/products/edit/<product_id>", methods=["GET", "POST"])
@role_required("seller", "admin")
def product_edit(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        abort(404)

    categories = product_service.get_categories()
    brands = product_service.get_brands()

    if request.method == "POST":
        updates = {
            "title": request.form.get("title", product["title"]),
            "price": float(request.form.get("price", product["price"])),
            "compare_at_price": float(request.form.get("compare_at_price", product.get("compare_at_price", product["price"]))),
            "stock": int(request.form.get("stock", product.get("stock", 0))),
            "summary": request.form.get("summary", product.get("summary", "")),
            "description": request.form.get("description", product.get("description", "")),
            "is_active": "is_active" in request.form,
        }
        product_service.update_product(product_id, updates)
        flash("Product updated successfully!", "success")
        return redirect(url_for("seller.products"))

    return render_template("seller/product_edit.html", product=product, categories=categories, brands=brands)


@seller_bp.route("/products/delete/<product_id>", methods=["POST"])
@role_required("seller", "admin")
def product_delete(product_id):
    product_service.delete_product(product_id)
    flash("Product listing deleted.", "info")
    return redirect(url_for("seller.products"))


@seller_bp.route("/products/<product_id>/variants", methods=["GET", "POST"])
@seller_bp.route("/products/variants/<product_id>", methods=["GET", "POST"])
@role_required("seller", "admin")
def product_variants(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        abort(404)

    if request.method == "POST":
        variant_name = request.form.get("variant_name")
        variant_color = request.form.get("variant_color", "#000000")
        variant_stock = int(request.form.get("variant_stock", 10))
        variant_price = float(request.form.get("variant_price", product["price"]))
        variant_sku = request.form.get("variant_sku", f"{product['sku']}-V")

        if "variants" not in product:
            product["variants"] = []

        product["variants"].append({
            "id": f"var-{len(product['variants']) + 1}",
            "name": variant_name,
            "color": variant_color,
            "stock": variant_stock,
            "price": variant_price,
            "sku": variant_sku,
        })
        flash(f"Variant '{variant_name}' added.", "success")
        return redirect(url_for("seller.product_variants", product_id=product_id))

    return render_template("seller/product_variants.html", product=product, variants=product.get("variants", []))


@seller_bp.route("/products/<product_id>/insights")
@seller_bp.route("/products/insights/<product_id>")
@role_required("seller", "admin")
def product_insights(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        abort(404)
    reviews = review_service.get_product_reviews(product_id)
    return render_template("seller/product_insights.html", product=product, reviews=reviews)


# --- ORDERS FULFILLMENT ---

@seller_bp.route("/orders")
@role_required("seller", "admin")
def orders():
    seller_id = _get_current_seller_id()
    seller_orders = order_service.get_orders_by_seller(seller_id)
    return render_template("seller/orders.html", orders=seller_orders)


@seller_bp.route("/orders/<order_id>")
@role_required("seller", "admin")
def order_detail(order_id):
    order = order_service.get_order_by_id(order_id)
    if not order:
        abort(404)
    seller_id = _get_current_seller_id()
    items = [item for item in order.get("items", []) if item.get("seller_id") == seller_id]
    if not items and auth_service.get_current_user().get("role") == "admin":
        items = order.get("items", [])
    seller_subtotal = sum(i["price"] * i["quantity"] for i in items)
    seller_commission = sum(i.get("commission_amount", 0) for i in items)
    seller_net = sum(i.get("seller_net_earning", 0) for i in items)
    return render_template(
        "seller/order_detail.html",
        order=order,
        items=items,
        seller_subtotal=seller_subtotal,
        seller_commission=seller_commission,
        seller_net=seller_net,
    )


@seller_bp.route("/orders/<order_id>/update-status", methods=["POST"])
@role_required("seller", "admin")
def order_update_status(order_id):
    new_status = request.form.get("status")
    carrier = request.form.get("carrier")
    tracking_number = request.form.get("tracking_number")
    order_service.update_order_status(order_id, new_status, carrier=carrier, tracking_number=tracking_number)
    flash(f"Order #{order_id} marked as {new_status.title()}.", "success")
    return redirect(url_for("seller.order_detail", order_id=order_id))


# --- INVENTORY & STOCK ---

@seller_bp.route("/inventory")
@role_required("seller", "admin")
def inventory():
    seller_id = _get_current_seller_id()
    inv_data = inventory_service.get_inventory_summary(seller_id=seller_id)
    logs = inventory_service.get_seller_logs(seller_id)
    return render_template("seller/inventory.html", logs=logs, **inv_data)


@seller_bp.route("/inventory/adjust", methods=["GET", "POST"])
@seller_bp.route("/inventory/adjust/<product_id>", methods=["GET", "POST"])
@role_required("seller", "admin")
def stock_adjust(product_id=None):
    seller_id = _get_current_seller_id()
    products = product_service.get_products_by_seller(seller_id)
    selected_product = None
    if product_id:
        selected_product = product_service.get_product_by_id(product_id)
    elif products:
        selected_product = products[0]

    if request.method == "POST":
        p_id = request.form.get("product_id", product_id)
        new_stock = int(request.form.get("new_stock", 0))
        reason = request.form.get("reason", "Manual adjustment")
        user = auth_service.get_current_user()
        adjusted_by = user["name"] if user else "Seller"

        prod = product_service.get_product_by_id(p_id)
        if prod:
            quantity_change = new_stock - prod["stock"]
            inventory_service.adjust_stock(
                product_id=p_id,
                quantity_change=quantity_change,
                reason=reason,
                adjusted_by=adjusted_by,
            )
            flash(f"Stock for '{prod['title']}' set to {new_stock} units.", "success")
        return redirect(url_for("seller.inventory"))

    return render_template("seller/stock_adjust.html", products=products, selected_product=selected_product)


# --- RETURNS & REFUNDS ---

@seller_bp.route("/returns")
@role_required("seller", "admin")
def returns():
    seller_id = _get_current_seller_id()
    seller_returns = [r for r in mock_store.returns if r.get("seller_id") == seller_id]
    return render_template("seller/returns.html", returns=seller_returns)


@seller_bp.route("/returns/<return_id>/action", methods=["POST"])
@role_required("seller", "admin")
def return_action(return_id):
    action = request.form.get("action")  # approve / reject
    ret = next((r for r in mock_store.returns if r["id"] == return_id), None)
    if ret:
        ret["status"] = "approved" if action == "approve" else "rejected"
        flash(f"Return {return_id} marked as {ret['status']}.", "info")
    return redirect(url_for("seller.returns"))


# --- EARNINGS & PAYOUTS ---

@seller_bp.route("/earnings")
@role_required("seller", "admin")
def earnings():
    seller_id = _get_current_seller_id()
    metrics = seller_service.get_seller_metrics(seller_id)
    payouts = payout_service.get_seller_payouts(seller_id)
    seller_orders = order_service.get_orders_by_seller(seller_id)
    return render_template("seller/earnings.html", metrics=metrics, payouts=payouts, orders=seller_orders, **metrics)


@seller_bp.route("/payouts")
@role_required("seller", "admin")
def payouts():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)
    payout_list = payout_service.get_seller_payouts(seller_id)
    return render_template("seller/payouts.html", seller=seller, payouts=payout_list)


@seller_bp.route("/payouts/request", methods=["GET", "POST"])
@role_required("seller", "admin")
def payout_request():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)

    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        bank_info = f"{seller['bank_account']['bank_name']} (A/C ...{seller['bank_account']['account_number'][-4:]})"
        try:
            payout = payout_service.request_payout(seller_id, amount, bank_info)
            flash(f"Payout request #{payout['id']} for ₹{amount:,.2f} submitted.", "success")
            return redirect(url_for("seller.payouts"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("seller/payout_request.html", seller=seller)


# --- STORE, REVIEWS, NOTIFICATIONS, SETTINGS, SUPPORT ---

@seller_bp.route("/store", methods=["GET", "POST"])
@role_required("seller", "admin")
def store():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)

    if request.method == "POST":
        updates = {
            "store_name": request.form.get("store_name", seller["store_name"]),
            "phone": request.form.get("phone", seller.get("phone", "")),
            "city": request.form.get("city", seller.get("city", "")),
            "state": request.form.get("state", seller.get("state", "")),
            "address": request.form.get("address", seller.get("address", "")),
        }
        seller_service.update_seller(seller_id, updates)
        flash("Store profile updated successfully.", "success")
        return redirect(url_for("seller.store"))

    products = product_service.list_products(seller_id=seller_id)
    return render_template("seller/store.html", seller=seller, products=products)


@seller_bp.route("/reviews")
@role_required("seller", "admin")
def reviews():
    seller_id = _get_current_seller_id()
    seller_reviews = review_service.get_seller_reviews(seller_id)
    return render_template("seller/reviews.html", reviews=seller_reviews)


@seller_bp.route("/reviews/<review_id>/reply", methods=["POST"])
@role_required("seller", "admin")
def review_reply(review_id):
    reply_text = request.form.get("reply", "").strip()
    review_service.reply_to_review(review_id, reply_text)
    flash("Reply published.", "success")
    return redirect(url_for("seller.reviews"))


@seller_bp.route("/notifications")
@role_required("seller", "admin")
def notifications():
    user = auth_service.get_current_user()
    user_id = user["id"] if user else "user-seller-1"
    notifs = notification_service.get_user_notifications(user_id, "seller")
    return render_template("seller/notifications.html", notifications=notifs)


@seller_bp.route("/settings", methods=["GET", "POST"])
@role_required("seller", "admin")
def settings():
    seller_id = _get_current_seller_id()
    seller = seller_service.get_seller_by_id(seller_id)
    if request.method == "POST":
        flash("Vendor preferences saved.", "success")
        return redirect(url_for("seller.settings"))
    return render_template("seller/settings.html", seller=seller)


@seller_bp.route("/support", methods=["GET", "POST"])
@role_required("seller", "admin")
def support():
    if request.method == "POST":
        flash("Support ticket dispatched to Nova Mart Partner Desk.", "success")
        return redirect(url_for("seller.support"))
    return render_template("seller/support.html")
