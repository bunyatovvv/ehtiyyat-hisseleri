from ..extensions import db


# ---- Mesaj şablonları ----
COUNTRY_CHOICES = [("AZ", "Azərbaycan"), ("GE", "Gürcüstan")]


def build_message(country: str, brand_name: str, part_name: str = "") -> str:
    """Ölkəyə görə WhatsApp mesajını qurur (AZ → Azərbaycanca, GE → Gürcücə)."""
    part_name = (part_name or "").strip()
    if country == "GE":
        if part_name:
            return f"გამარჯობა, {brand_name}-ისთვის {part_name} მჭირდება."
        return f"გამარჯობა, {brand_name}-ისთვის სათადარიგო ნაწილი მჭირდება."

    # Default → AZ
    if part_name:
        return f"Salam, {brand_name} üçün {part_name} lazımdır."
    return f"Salam, {brand_name} üçün ehtiyat hissəsi lazımdır."

# --- Many-to-many: mağaza ↔ markalar ---
store_brands = db.Table(
    "store_brands",
    db.Column("store_id", db.Integer, db.ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True),
    db.Column("brand_id", db.Integer, db.ForeignKey("brands.id", ondelete="CASCADE"), primary_key=True),
)


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(80), nullable=True, index=True)
    # "AZ" = Azərbaycan, "GE" = Gürcüstan — mesaj dilini bu təyin edir
    country = db.Column(db.String(2), nullable=False, default="AZ", index=True)
    phone = db.Column(db.String(40), nullable=True)
    whatsapp_number = db.Column(db.String(40), nullable=False)
    working_hours = db.Column(db.String(120), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    brands = db.relationship(
        "Brand",
        secondary=store_brands,
        backref=db.backref("stores", lazy="dynamic"),
        lazy="selectin",
    )

    @property
    def whatsapp_digits(self) -> str:
        """wa.me link üçün rəqəm-only nömrə (+ və ayırıcılar təmizlənir)."""
        if not self.whatsapp_number:
            return ""
        return "".join(ch for ch in self.whatsapp_number if ch.isdigit())

    def whatsapp_message(self, brand_name: str, part_name: str = "") -> str:
        """Mağazanın ölkəsinə uyğun dildə WhatsApp mesajı qurur."""
        return build_message(self.country, brand_name, part_name)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Store {self.name}>"
