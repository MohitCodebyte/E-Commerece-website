"""
Authentication Routes (/auth)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import auth_service
from app.repositories import user_repo, seller_repo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role_hint = request.form.get("role", "customer")

        user = auth_service.authenticate(email, password)
        if user:
            auth_service.login_user(user)
            flash(f"Welcome back, {user['name']}!", "success")
            
            # Redirect by role
            next_url = request.args.get("next")
            if next_url:
                return redirect(next_url)

            if user["role"] == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user["role"] == "seller":
                return redirect(url_for("seller.dashboard"))
            else:
                return redirect(url_for("customer.home"))
        else:
            flash("Invalid email or password. Please try demo accounts.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()

        try:
            user = auth_service.register_customer(name=name, email=email, password=password, phone=phone)
            auth_service.login_user(user)
            flash("Registration successful! Welcome to Nova Mart.", "success")
            return redirect(url_for("customer.home"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("auth/register.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        flash(f"Password reset link has been sent to {email} (Demo simulation).", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot_password.html")


@auth_bp.route("/logout")
def logout():
    auth_service.logout_user()
    flash("You have been securely logged out.", "info")
    return redirect(url_for("customer.home"))


@auth_bp.route("/switch-demo-role/<role>")
def switch_demo_role(role):
    """Convenient demo role switcher for testing all 3 user roles instantly."""
    if role == "customer":
        user = user_repo.get_by_email("customer@novamart.in")
        target_route = "customer.home"
    elif role == "seller":
        user = user_repo.get_by_email("seller@techzone.in")
        target_route = "seller.dashboard"
    elif role == "admin":
        user = user_repo.get_by_email("admin@novamart.in")
        target_route = "admin.dashboard"
    else:
        flash("Unknown role requested.", "error")
        return redirect(url_for("customer.home"))

    if user:
        auth_service.login_user(user)
        flash(f"Switched session to {user['name']} ({role.upper()} Mode)", "success")
        return redirect(url_for(target_route))

    flash("Demo user not found.", "error")
    return redirect(url_for("customer.home"))
