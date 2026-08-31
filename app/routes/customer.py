"""
Customer Portal Routes (Frontend UI & Customer Account)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, abort
from app.services import (
    product_service,
    cart_service,
    order_service,
    review_service,
    notification_service,
    auth_service,
)
from app.repositories import user_repo
from app.utils.decorators import login_required

customer_bp = Blueprint("customer", __name__)


# --- PUBLIC CATALOG ROUTES ---

@customer_bp.route("/")
def home():
    featured_products = product_service.get_featured_products(limit=4)
    all_products = product_service.list_products(limit=8)
    categories = product_service.get_categories()
    brands = product_service.get_brands()
    return render_template(
        "customer/home.html",
        featured_products=featured_products,
        products=all_products,
        categories=categories,
        brands=brands,
    )


@customer_bp.route("/shop")
def shop():
    category = request.args.get("category")
    brand = request.args.get("brand")
    sort_by = request.args.get("sort", "featured")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    products = product_service.list_products(
        category=category,
        brand=brand,
        sort_by=sort_by,
        min_price=min_price,
        max_price=max_price,
    )
    categories = product_service.get_categories()
    brands = product_service.get_brands()

    return render_template(
        "customer/shop.html",
        products=products,
        categories=categories,
        brands=brands,
        selected_category=category,
        selected_brand=brand,
        selected_sort=sort_by,
        min_price=min_price,
        max_price=max_price,
    )


@customer_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    category = request.args.get("category")
    sort_by = request.args.get("sort", "featured")

    products = product_service.list_products(
        query=query,
        category=category,
        sort_by=sort_by,
    )
    categories = product_service.get_categories()

    return render_template(
        "customer/search.html",
        query=query,
        products=products,
        categories=categories,
        total_results=len(products),
    )


@customer_bp.route("/category/<slug>")
def category(slug):
    cat = product_service.get_category_by_slug(slug)
    if not cat:
        abort(404)

    sort_by = request.args.get("sort", "featured")
    products = product_service.list_products(category=slug, sort_by=sort_by)
    brands = product_service.get_brands()

    return render_template(
        "customer/category.html",
        category=cat,
        products=products,
        brands=brands,
        selected_sort=sort_by,
    )


@customer_bp.route("/product/<slug>")
def product_detail(slug):
    product = product_service.get_product_by_slug(slug)
    if not product:
        abort(404)

    reviews = review_service.get_product_reviews(product["id"])
    related_products = product_service.list_products(category=product.get("category_id"), limit=4)
    # filter out the current product from related
    related_products = [p for p in related_products if p["id"] != product["id"]]

    in_wishlist = cart_service.is_in_wishlist(product["id"])

    return render_template(
        "customer/product_detail.html",
        product=product,
        reviews=reviews,
        related_products=related_products,
        in_wishlist=in_wishlist,
    )


# --- CART & WISHLIST ROUTES ---

@customer_bp.route("/cart")
def cart():
    cart_details = cart_service.get_cart_details()
    return render_template("customer/cart.html", cart=cart_details)


@customer_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    variant_id = request.form.get("variant_id")

    try:
        cart_details = cart_service.add_to_cart(product_id, quantity, variant_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
            return jsonify({"success": True, "cart": cart_details})
        flash("Item added to your shopping cart!", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(request.referrer or url_for("customer.cart"))


@customer_bp.route("/cart/update", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    variant_id = request.form.get("variant_id")

    cart_details = cart_service.update_quantity(product_id, quantity, variant_id)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": True, "cart": cart_details})
    
    return redirect(url_for("customer.cart"))


@customer_bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    product_id = request.form.get("product_id")
    variant_id = request.form.get("variant_id")

    cart_service.remove_from_cart(product_id, variant_id)
    flash("Item removed from cart.", "info")
    return redirect(url_for("customer.cart"))


@customer_bp.route("/cart/apply-coupon", methods=["POST"])
def apply_coupon():
    code = request.form.get("coupon_code", "").strip()
    try:
        cart_service.apply_coupon(code)
        flash(f"Coupon '{code.upper()}' applied successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("customer.cart"))


@customer_bp.route("/cart/remove-coupon", methods=["POST"])
def remove_coupon():
    cart_service.remove_coupon()
    flash("Coupon removed.", "info")
    return redirect(url_for("customer.cart"))


@customer_bp.route("/wishlist")
def wishlist():
    items = cart_service.get_wishlist_items()
    return render_template("customer/wishlist.html", items=items)


@customer_bp.route("/wishlist/toggle", methods=["POST"])
def toggle_wishlist():
    product_id = request.form.get("product_id")
    is_in_wishlist = cart_service.toggle_wishlist(product_id)
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": True, "in_wishlist": is_in_wishlist})

    msg = "Added to wishlist." if is_in_wishlist else "Removed from wishlist."
    flash(msg, "info")
    return redirect(request.referrer or url_for("customer.wishlist"))


# --- CHECKOUT & ORDER ROUTES ---

@customer_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_details = cart_service.get_cart_details()
    if not cart_details["items"]:
        flash("Your cart is empty. Please add items before checking out.", "warning")
        return redirect(url_for("customer.shop"))

    user = auth_service.get_current_user()
    addresses = user.get("addresses", []) if user else []

    if request.method == "POST":
        # Process order placement
        recipient = request.form.get("recipient")
        street = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        pincode = request.form.get("pincode")
        phone = request.form.get("phone")
        payment_method = request.form.get("payment_method", "UPI (Google Pay / PhonePe)")

        shipping_address = {
            "recipient": recipient,
            "street": street,
            "city": city,
            "state": state,
            "pincode": pincode,
            "phone": phone,
        }

        customer_info = user or {
            "id": "guest",
            "name": recipient,
            "email": request.form.get("email", "guest@novamart.in"),
            "phone": phone,
        }

        try:
            order = order_service.place_order(
                customer=customer_info,
                shipping_address=shipping_address,
                payment_method=payment_method,
            )
            flash("Order placed successfully!", "success")
            return redirect(url_for("customer.order_success", order_id=order["id"]))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("customer/checkout.html", cart=cart_details, addresses=addresses, user=user)


@customer_bp.route("/order-success/<order_id>")
def order_success(order_id):
    order = order_service.get_order_by_id(order_id)
    if not order:
        abort(404)
    return render_template("customer/order_success.html", order=order)


# --- CUSTOMER ACCOUNT ROUTES ---

@customer_bp.route("/customer/account")
@login_required
def account():
    user = auth_service.get_current_user()
    orders = order_service.get_orders_by_customer(user["id"])
    recent_orders = orders[:3]
    notifications = notification_service.get_user_notifications(user["id"], "customer")
    return render_template(
        "customer/account.html",
        user=user,
        recent_orders=recent_orders,
        total_orders=len(orders),
        notifications=notifications[:4],
    )


@customer_bp.route("/customer/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = auth_service.get_current_user()
    if request.method == "POST":
        updates = {
            "name": request.form.get("name", user["name"]),
            "phone": request.form.get("phone", user.get("phone", "")),
        }
        new_password = request.form.get("new_password")
        if new_password:
            updates["password"] = new_password

        user_repo.update(user["id"], updates)
        flash("Profile updated successfully!", "success")
        return redirect(url_for("customer.profile"))

    return render_template("customer/profile.html", user=user)


@customer_bp.route("/customer/addresses", methods=["GET", "POST"])
@login_required
def addresses():
    user = auth_service.get_current_user()
    if request.method == "POST":
        addr_data = {
            "label": request.form.get("label", "Home"),
            "recipient": request.form.get("recipient", user["name"]),
            "phone": request.form.get("phone", user.get("phone", "")),
            "street": request.form.get("street", ""),
            "city": request.form.get("city", ""),
            "state": request.form.get("state", ""),
            "pincode": request.form.get("pincode", ""),
            "is_default": "is_default" in request.form,
        }
        user_repo.add_address(user["id"], addr_data)
        flash("Address saved successfully.", "success")
        return redirect(url_for("customer.addresses"))

    user_addresses = user.get("addresses", [])
    return render_template("customer/addresses.html", addresses=user_addresses, user=user)


@customer_bp.route("/customer/orders")
@login_required
def orders():
    user = auth_service.get_current_user()
    user_orders = order_service.get_orders_by_customer(user["id"])
    return render_template("customer/orders.html", orders=user_orders)


@customer_bp.route("/customer/order/<order_id>")
@customer_bp.route("/customer/orders/<order_id>")
@login_required
def order_detail(order_id):
    order = order_service.get_order_by_id(order_id)
    if not order:
        abort(404)
    return render_template("customer/order_detail.html", order=order)


@customer_bp.route("/customer/track-order")
def track_order():
    order_id = request.args.get("order_id", "").strip()
    order = None
    if order_id:
        order = order_service.get_order_by_id(order_id)
        if not order:
            flash(f"Order #{order_id} not found. Please verify your tracking number.", "warning")
    else:
        # Default to first order if logged in
        user = auth_service.get_current_user()
        if user:
            user_orders = order_service.get_orders_by_customer(user["id"])
            if user_orders:
                order = user_orders[0]

    return render_template("customer/track_order.html", order=order, query_id=order_id)


@customer_bp.route("/customer/reviews")
@login_required
def reviews():
    user = auth_service.get_current_user()
    user_reviews = review_service.get_user_reviews(user["id"])
    return render_template("customer/reviews.html", reviews=user_reviews)


@customer_bp.route("/customer/write-review/<product_id>", methods=["GET", "POST"])
@customer_bp.route("/customer/reviews/write/<product_id>", methods=["GET", "POST"])
@login_required
def write_review(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        abort(404)

    user = auth_service.get_current_user()
    if request.method == "POST":
        rating = int(request.form.get("rating", 5))
        title = request.form.get("title", "")
        comment = request.form.get("comment", "")

        review_service.add_review(
            user=user,
            product_id=product_id,
            rating=rating,
            title=title,
            comment=comment,
        )
        flash("Thank you! Your review has been submitted.", "success")
        return redirect(url_for("customer.product_detail", slug=product["slug"]))

    return render_template("customer/write_review.html", product=product)


@customer_bp.route("/customer/notifications")
@login_required
def notifications():
    user = auth_service.get_current_user()
    notifs = notification_service.get_user_notifications(user["id"], "customer")
    return render_template("customer/notifications.html", notifications=notifs)


@customer_bp.route("/customer/returns", methods=["GET", "POST"])
@login_required
def returns():
    user = auth_service.get_current_user()
    from app.repositories.mock.store import mock_store
    user_returns = [r for r in mock_store.returns if r.get("customer_id") == user["id"]]
    user_orders = order_service.get_orders_by_customer(user["id"])

    if request.method == "POST":
        order_id = request.form.get("order_id")
        reason = request.form.get("reason")
        comments = request.form.get("comments")

        order = order_service.get_order_by_id(order_id)
        if order:
            new_ret = {
                "id": f"RET-2024-{len(mock_store.returns) + 10:02d}",
                "order_id": order_id,
                "customer_id": user["id"],
                "customer_name": user["name"],
                "seller_id": order["items"][0]["seller_id"] if order.get("items") else "seller-1",
                "seller_name": order["items"][0]["seller_name"] if order.get("items") else "TechZone Electronics",
                "product_id": order["items"][0]["product_id"] if order.get("items") else "prod-1",
                "product_title": order["items"][0]["product_title"] if order.get("items") else "Product",
                "reason": reason,
                "amount": order.get("total", 0.0),
                "status": "requested",
                "request_date": "2024-08-31",
                "resolution_date": None,
                "comments": comments,
            }
            mock_store.returns.insert(0, new_ret)
            flash("Your return request has been submitted for seller approval.", "success")
            return redirect(url_for("customer.returns"))

    return render_template("customer/returns.html", returns=user_returns, orders=user_orders)


@customer_bp.route("/customer/support", methods=["GET", "POST"])
def support():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        flash("Thank you for contacting Nova Mart Support. Our care team will reply within 24 hours.", "success")
        return redirect(url_for("customer.support"))

    return render_template("customer/support.html")
