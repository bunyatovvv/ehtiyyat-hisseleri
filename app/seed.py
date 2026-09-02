"""İlkin test datası."""
import os

from .extensions import db
from .models import AdminUser, Brand, Store


def seed_if_empty() -> None:
    """Baza boşdursa test datası əlavə edir."""
    if db.session.query(Brand).count() > 0:
        return

    # --- Markalar ---
    brand_names = [
        "Audi", "BMW", "Mercedes", "Volkswagen", "Porsche", "Opel",
        "Toyota", "Honda", "Nissan", "Mazda", "Lexus", "Mitsubishi",
        "Hyundai", "Kia",
        "Ford", "Chevrolet", "Chrysler",
        "Peugeot", "Renault", "Citroen",
        "Skoda", "Volvo", "Land Rover",
    ]
    brands = {name: Brand(name=name) for name in brand_names}
    db.session.add_all(brands.values())
    db.session.flush()

    # --- Mağazalar (AZ = Azərbaycan, GE = Gürcüstan) ---
    stores_data = [
        # ==== Azərbaycan ====
        {
            "name": "Alman Auto Parts",
            "country": "AZ",
            "address": "H.Əliyev pr. 25",
            "city": "Bakı",
            "phone": "+994 12 555 10 20",
            "whatsapp_number": "+994 50 555 10 20",
            "working_hours": "09:00 - 19:00",
            "notes": "Alman markaları üzrə ixtisaslaşıb.",
            "brands": ["Audi", "BMW", "Mercedes", "Volkswagen", "Porsche"],
        },
        {
            "name": "Yapon Ehtiyat",
            "country": "AZ",
            "address": "Nizami küç. 14",
            "city": "Bakı",
            "phone": "+994 12 444 33 22",
            "whatsapp_number": "+994 55 444 33 22",
            "working_hours": "10:00 - 20:00",
            "notes": "Yapon markaları üçün geniş çeşid.",
            "brands": ["Toyota", "Honda", "Nissan", "Mazda", "Lexus", "Mitsubishi"],
        },
        {
            "name": "Universal Auto",
            "country": "AZ",
            "address": "Şəhriyar 3",
            "city": "Sumqayıt",
            "phone": "+994 18 655 10 10",
            "whatsapp_number": "+994 51 655 10 10",
            "working_hours": "09:00 - 18:00",
            "notes": "Əsas markalar üçün ehtiyat hissələri.",
            "brands": ["Audi", "BMW", "Toyota", "Hyundai", "Kia", "Ford"],
        },
        {
            "name": "Mercedes Pro",
            "country": "AZ",
            "address": "Cavadxan küç. 88",
            "city": "Gəncə",
            "phone": "+994 22 256 78 90",
            "whatsapp_number": "+994 70 256 78 90",
            "working_hours": "09:00 - 19:00",
            "notes": "Yalnız Mercedes üçün.",
            "brands": ["Mercedes"],
        },
        {
            "name": "BMW Center",
            "country": "AZ",
            "address": "M.Ə.Rəsulzadə 45",
            "city": "Bakı",
            "phone": "+994 12 333 22 11",
            "whatsapp_number": "+994 55 333 22 11",
            "working_hours": "10:00 - 20:00",
            "notes": "BMW orijinal və analoq hissələr.",
            "brands": ["BMW"],
        },
        {
            "name": "Hyundai / Kia World",
            "country": "AZ",
            "address": "İstiqlaliyyət 12",
            "city": "Bakı",
            "phone": "+994 12 987 65 43",
            "whatsapp_number": "+994 77 987 65 43",
            "working_hours": "09:00 - 18:00",
            "notes": "Koreya markaları üzrə orijinal hissələr.",
            "brands": ["Hyundai", "Kia"],
        },
        {
            "name": "Fransız Auto",
            "country": "AZ",
            "address": "Nərimanov pr. 55",
            "city": "Bakı",
            "phone": "+994 12 222 44 66",
            "whatsapp_number": "+994 55 222 44 66",
            "working_hours": "09:00 - 19:00",
            "notes": "Fransız markaları üçün ixtisaslaşmış mağaza.",
            "brands": ["Peugeot", "Renault", "Citroen"],
        },
        {
            "name": "Sumqayıt Auto",
            "country": "AZ",
            "address": "S.Vurğun 41",
            "city": "Sumqayıt",
            "phone": "+994 18 444 55 66",
            "whatsapp_number": "+994 55 444 55 66",
            "working_hours": "09:00 - 19:00",
            "notes": "Regionda geniş çeşid.",
            "brands": ["Audi", "Mercedes", "Hyundai", "Volkswagen", "Skoda"],
        },
        # ==== Gürcüstan ====
        {
            "name": "Tbilisi Auto Parts",
            "country": "GE",
            "address": "Rustaveli Ave. 12",
            "city": "Tbilisi",
            "phone": "+995 32 200 10 10",
            "whatsapp_number": "+995 599 10 20 30",
            "working_hours": "09:00 - 19:00",
            "notes": "დიდი ასორტიმენტი გერმანული მარკებისთვის.",
            "brands": ["Audi", "BMW", "Mercedes", "Volkswagen", "Porsche"],
        },
        {
            "name": "Kavkaz Motors",
            "country": "GE",
            "address": "Aghmashenebeli Ave. 88",
            "city": "Tbilisi",
            "phone": "+995 32 555 66 77",
            "whatsapp_number": "+995 577 88 99 00",
            "working_hours": "10:00 - 20:00",
            "notes": "იაპონური და კორეული ავტომობილები.",
            "brands": ["Toyota", "Honda", "Nissan", "Hyundai", "Kia", "Lexus"],
        },
        {
            "name": "Batumi Auto",
            "country": "GE",
            "address": "Chavchavadze St. 34",
            "city": "Batumi",
            "phone": "+995 422 27 55 44",
            "whatsapp_number": "+995 555 12 34 56",
            "working_hours": "09:00 - 19:00",
            "notes": "შავი ზღვის რეგიონში მთავარი მაღაზია.",
            "brands": ["BMW", "Toyota", "Ford", "Chevrolet", "Volvo"],
        },
        {
            "name": "Kutaisi Parts",
            "country": "GE",
            "address": "Tamar Mepe St. 5",
            "city": "Kutaisi",
            "phone": "+995 431 24 55 66",
            "whatsapp_number": "+995 599 44 55 66",
            "working_hours": "09:00 - 18:00",
            "notes": "დასავლეთ საქართველოს ცენტრი.",
            "brands": ["Mercedes", "Opel", "Renault", "Peugeot", "Skoda"],
        },
    ]

    for data in stores_data:
        store = Store(
            name=data["name"],
            country=data.get("country", "AZ"),
            address=data["address"],
            city=data["city"],
            phone=data["phone"],
            whatsapp_number=data["whatsapp_number"],
            working_hours=data["working_hours"],
            notes=data["notes"],
            is_active=True,
        )
        store.brands = [brands[b] for b in data["brands"]]
        db.session.add(store)

    # --- Admin istifadəçi ---
    if db.session.query(AdminUser).count() == 0:
        admin = AdminUser(username=os.getenv("ADMIN_USERNAME", "admin"))
        admin.set_password(os.getenv("ADMIN_PASSWORD", "admin123"))
        db.session.add(admin)

    db.session.commit()
