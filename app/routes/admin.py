"""Admin panel route-ları — Flask-Login ilə qorunur."""
from typing import Tuple

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, or_

from ..extensions import db
from ..models import AdminUser, Brand, Store

admin_bp = Blueprint("admin", __name__)


# ---------------- Auth ----------------

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        user = db.session.query(AdminUser).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Uğurla daxil oldunuz.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))

        flash("İstifadəçi adı və ya parol yanlışdır.", "danger")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sistemdən çıxdınız.", "info")
    return redirect(url_for("admin.login"))


# ---------------- Dashboard ----------------

@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "brands": db.session.query(func.count(Brand.id)).scalar() or 0,
        "stores": db.session.query(func.count(Store.id)).scalar() or 0,
        "active_stores": db.session.query(func.count(Store.id))
        .filter(Store.is_active.is_(True))
        .scalar()
        or 0,
    }
    return render_template("admin/dashboard.html", stats=stats)


# ---------------- Brands CRUD ----------------

@admin_bp.route("/brands")
@login_required
def brand_list():
    brands = db.session.query(Brand).order_by(Brand.name).all()
    return render_template("admin/brands/list.html", brands=brands)


@admin_bp.route("/brands/new", methods=["GET", "POST"])
@login_required
def brand_new():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Ad boş ola bilməz.", "danger")
        elif db.session.query(Brand).filter(func.lower(Brand.name) == name.lower()).first():
            flash("Bu adda marka artıq mövcuddur.", "danger")
        else:
            db.session.add(Brand(name=name))
            db.session.commit()
            flash("Marka əlavə olundu.", "success")
            return redirect(url_for("admin.brand_list"))

    return render_template("admin/brands/form.html", brand=None)


@admin_bp.route("/brands/<int:brand_id>/edit", methods=["GET", "POST"])
@login_required
def brand_edit(brand_id: int):
    brand = db.session.get(Brand, brand_id) or abort(404)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Ad boş ola bilməz.", "danger")
        else:
            duplicate = (
                db.session.query(Brand)
                .filter(func.lower(Brand.name) == name.lower(), Brand.id != brand.id)
                .first()
            )
            if duplicate:
                flash("Bu adda başqa marka var.", "danger")
            else:
                brand.name = name
                db.session.commit()
                flash("Marka yeniləndi.", "success")
                return redirect(url_for("admin.brand_list"))

    return render_template("admin/brands/form.html", brand=brand)


@admin_bp.route("/brands/<int:brand_id>/delete", methods=["POST"])
@login_required
def brand_delete(brand_id: int):
    brand = db.session.get(Brand, brand_id) or abort(404)
    db.session.delete(brand)
    db.session.commit()
    flash("Marka silindi.", "info")
    return redirect(url_for("admin.brand_list"))


# ---------------- Stores CRUD ----------------

@admin_bp.route("/stores")
@login_required
def store_list():
    q = (request.args.get("q") or "").strip()
    brand_id = request.args.get("brand_id", type=int)
    city = (request.args.get("city") or "").strip()
    country = (request.args.get("country") or "").strip().upper()
    status = request.args.get("status")  # "active", "inactive", "" (hamısı)

    query = db.session.query(Store)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Store.name.ilike(like),
                Store.address.ilike(like),
                Store.phone.ilike(like),
                Store.whatsapp_number.ilike(like),
            )
        )
    if brand_id:
        query = query.filter(Store.brands.any(Brand.id == brand_id))
    if city:
        query = query.filter(Store.city == city)
    if country in ("AZ", "GE"):
        query = query.filter(Store.country == country)
    if status == "active":
        query = query.filter(Store.is_active.is_(True))
    elif status == "inactive":
        query = query.filter(Store.is_active.is_(False))

    stores = query.order_by(Store.name).all()

    brands = db.session.query(Brand).order_by(Brand.name).all()
    cities = [
        row[0]
        for row in db.session.query(Store.city)
        .filter(Store.city.isnot(None), Store.city != "")
        .distinct()
        .order_by(Store.city)
        .all()
    ]

    return render_template(
        "admin/stores/list.html",
        stores=stores,
        brands=brands,
        cities=cities,
        filters={
            "q": q,
            "brand_id": brand_id,
            "city": city,
            "country": country,
            "status": status or "",
        },
    )


def _store_from_form(store: Store, form) -> Tuple[bool, str]:
    """Form datasını Store obyektinə köçürür. (ok, error_message) qaytarır."""
    name = (form.get("name") or "").strip()
    whatsapp_number = (form.get("whatsapp_number") or "").strip()

    if not name:
        return False, "Ad boş ola bilməz."
    if not whatsapp_number:
        return False, "WhatsApp nömrəsi boş ola bilməz."

    country = (form.get("country") or "AZ").strip().upper()
    if country not in ("AZ", "GE"):
        country = "AZ"

    store.name = name
    store.country = country
    store.address = (form.get("address") or "").strip() or None
    store.city = (form.get("city") or "").strip() or None
    store.phone = (form.get("phone") or "").strip() or None
    store.whatsapp_number = whatsapp_number
    store.working_hours = (form.get("working_hours") or "").strip() or None
    store.notes = (form.get("notes") or "").strip() or None
    store.is_active = form.get("is_active") == "on"

    brand_ids = [int(bid) for bid in form.getlist("brand_ids") if bid.isdigit()]
    store.brands = (
        db.session.query(Brand).filter(Brand.id.in_(brand_ids)).all() if brand_ids else []
    )
    return True, ""


@admin_bp.route("/stores/new", methods=["GET", "POST"])
@login_required
def store_new():
    brands = db.session.query(Brand).order_by(Brand.name).all()

    if request.method == "POST":
        store = Store(whatsapp_number="", country="AZ")  # NOT NULL üçün placeholder
        ok, err = _store_from_form(store, request.form)
        if not ok:
            flash(err, "danger")
        else:
            db.session.add(store)
            db.session.commit()
            flash("Mağaza əlavə olundu.", "success")
            return redirect(url_for("admin.store_list"))

        # xəta olduqda formu doldurulmuş vəziyyətdə geri qaytarırıq
        return render_template(
            "admin/stores/form.html",
            store=store,
            brands=brands,
            selected_brand_ids={b.id for b in store.brands},
        )

    return render_template(
        "admin/stores/form.html",
        store=None,
        brands=brands,
        selected_brand_ids=set(),
    )


@admin_bp.route("/stores/<int:store_id>/edit", methods=["GET", "POST"])
@login_required
def store_edit(store_id: int):
    store = db.session.get(Store, store_id) or abort(404)
    brands = db.session.query(Brand).order_by(Brand.name).all()

    if request.method == "POST":
        ok, err = _store_from_form(store, request.form)
        if not ok:
            flash(err, "danger")
        else:
            db.session.commit()
            flash("Mağaza yeniləndi.", "success")
            return redirect(url_for("admin.store_list"))

    return render_template(
        "admin/stores/form.html",
        store=store,
        brands=brands,
        selected_brand_ids={b.id for b in store.brands},
    )


@admin_bp.route("/stores/<int:store_id>/delete", methods=["POST"])
@login_required
def store_delete(store_id: int):
    store = db.session.get(Store, store_id) or abort(404)
    db.session.delete(store)
    db.session.commit()
    flash("Mağaza silindi.", "info")
    return redirect(url_for("admin.store_list"))


@admin_bp.route("/stores/<int:store_id>/toggle", methods=["POST"])
@login_required
def store_toggle(store_id: int):
    store = db.session.get(Store, store_id) or abort(404)
    store.is_active = not store.is_active
    db.session.commit()
    flash(
        f"Mağaza {'aktivləşdirildi' if store.is_active else 'deaktiv edildi'}.",
        "success" if store.is_active else "warning",
    )
    next_url = request.form.get("next") or url_for("admin.store_list")
    return redirect(next_url)
