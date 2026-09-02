"""İşçi tərəfi (public) route-ları — login tələb olunmur."""
from urllib.parse import quote

from flask import Blueprint, render_template, request

from ..extensions import db
from ..models import Brand, Store
from ..models.store import build_message

public_bp = Blueprint("public", __name__)


@public_bp.route("/", methods=["GET"])
def index():
    """Marka seçimi + sərbəst hissə adı → uyğun mağazalar."""
    brands = db.session.query(Brand).order_by(Brand.name).all()

    brand_id = request.args.get("brand_id", type=int)
    part_name = (request.args.get("part_name") or "").strip()
    country = (request.args.get("country") or "").strip().upper()
    if country not in ("AZ", "GE"):
        country = ""  # boş = hamısı

    selected_brand = None
    stores = []
    preview_az = ""
    preview_ge = ""
    has_az = False
    has_ge = False

    if brand_id:
        selected_brand = db.session.get(Brand, brand_id)

    if selected_brand:
        query = (
            db.session.query(Store)
            .filter(Store.is_active.is_(True))
            .filter(Store.brands.any(Brand.id == selected_brand.id))
        )
        if country:
            query = query.filter(Store.country == country)
        stores = query.order_by(Store.country, Store.name).all()

        has_az = any(s.country == "AZ" for s in stores)
        has_ge = any(s.country == "GE" for s in stores)

        if has_az:
            preview_az = build_message("AZ", selected_brand.name, part_name)
        if has_ge:
            preview_ge = build_message("GE", selected_brand.name, part_name)

    # Hər mağaza üçün ilkin (JS-siz) mesaj + encoded URL — templatedə istifadə olunur.
    def store_msg(s):
        return build_message(s.country, selected_brand.name, part_name) if selected_brand else ""

    store_messages = {s.id: store_msg(s) for s in stores}
    store_messages_encoded = {sid: quote(msg) for sid, msg in store_messages.items()}

    return render_template(
        "public/index.html",
        brands=brands,
        selected_brand=selected_brand,
        part_name=part_name,
        stores=stores,
        preview_az=preview_az,
        preview_ge=preview_ge,
        has_az=has_az,
        has_ge=has_ge,
        store_messages=store_messages,
        store_messages_encoded=store_messages_encoded,
        selected_country=country,
    )
