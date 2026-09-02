# Ehtiyat hissələri

Maşın ehtiyat hissələri satan mağazaları idarə etmək üçün daxili (lokal şəbəkədə istifadə üçün) veb tətbiq. İşçilər avtomobil markasını seçir, uyğun mağazaların siyahısını görür və birbaşa WhatsApp-dan mağazaya yaza bilir. Mağazalar Azərbaycan və Gürcüstanda ola bilər — WhatsApp mesajı avtomatik olaraq mağazanın ölkəsinə uyğun dildə (Azərbaycanca / Gürcücə) hazırlanır.

## Texniki stack

- **Backend:** Python 3.9+, Flask 3, Flask-SQLAlchemy, Flask-Login, Flask-WTF (CSRF)
- **Verilənlər bazası:** SQLite (SQLAlchemy ORM)
- **Frontend:** Jinja2 template + Bootstrap 5 (CDN-dən), sadə vanilla JS
- **Build addımı yoxdur** — `pip install` və `python app.py` kifayətdir.

## Layihə strukturu

```
.
├── app.py                     # Giriş nöqtəsi
├── requirements.txt
├── .env.example               # Konfiqurasiya nümunəsi
├── README.md
└── app/
    ├── __init__.py            # Flask factory
    ├── extensions.py          # db / login_manager / csrf
    ├── seed.py                # İlkin test datası
    ├── models/
    │   ├── admin_user.py
    │   ├── brand.py
    │   └── store.py           # ölkə + WhatsApp mesaj şablonları
    ├── routes/
    │   ├── admin.py           # /admin/* – login qorumalı
    │   └── public.py          # /  – işçi tərəfi
    ├── static/css/app.css
    └── templates/
        ├── base.html
        ├── admin/…            # login, dashboard, brands, stores
        └── public/…           # işçi tərəfi
```

## Verilənlər bazası sxemi

- `brands` (id, name)
- `stores` (id, name, address, city, **country** [AZ/GE], phone, whatsapp_number, working_hours, notes, is_active)
- `store_brands` (store_id, brand_id) — many-to-many
- `admin_users` (id, username, password_hash)

Parollar `werkzeug.security` (`pbkdf2:sha256`) ilə hash edilir. Bütün SQL sorğuları SQLAlchemy ORM (parametrized) vasitəsilə icra olunur — SQL injection-a qarşı təhlükəsizdir. Bütün POST formalarında CSRF token yoxlanılır.

## İşə salmaq

### 1. Asılılıqları qur

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Konfiqurasiya

`.env.example` faylını `.env` olaraq kopyalayın və `SECRET_KEY`, admin adı/parolunu dəyişin:

```bash
cp .env.example .env
```

### 3. Tətbiqi işə sal

```bash
python app.py
```

İlk işə salınmada:
- `ehtiyat_hisseleri.db` avtomatik yaradılır,
- test datası (23 marka, 12 mağaza — 8 AZ + 4 GE) yüklənir,
- admin istifadəçisi yaradılır: **admin / admin123** (və ya `.env`-də verdiyiniz dəyərlər).

Sonra brauzerdə açın: <http://127.0.0.1:5001>

- İşçi tərəfi: `/`
- Admin: `/admin/login`

> macOS-da 5000 portu AirPlay Receiver tərəfindən tutulur, ona görə default port **5001**-dir.

## İstifadə

### İşçi tərəfi (`/`)
1. **Marka** seçin (dropdown və ya kart üzərinə klik).
2. **Ölkə** filtrini istəyə görə seçin (Hamısı / 🇦🇿 AZ / 🇬🇪 GE).
3. **Hissənin adı** sahəsinə hissənin təsvirini yazın (məs. *BMW F30 kondisioner klapanı*) — yaza-yaza WhatsApp mesajının önizləməsi canlı yenilənir.
4. Aktiv mağazaların siyahısından:
   - **WhatsApp-da yaz** — tək mağazaya klik anında textbox-un cari dəyəri ilə mesaj göndərilir.
   - **Hamısını seç** + **Seçilmişlərə göndər** — seçilən mağazalar üçün ardıcıl WhatsApp tab-ları açılır. Hər mağazaya öz ölkəsinin dilində mesaj gedir.

Mesaj formatı:
- 🇦🇿 AZ: `Salam, {marka} üçün {hissə} lazımdır.`
- 🇬🇪 GE: `გამარჯობა, {marka}-ისთვის {part} მჭირდება.`

### Admin (`/admin`)
- **Dashboard** — marka/mağaza sayları.
- **Markalar** — tam CRUD.
- **Mağazalar** — tam CRUD; ad/ünvan/telefon üzrə axtarış, marka/ölkə/şəhər/status üzrə filtr, tez aktiv/deaktiv toggle.

## 2 kompüter arasında ortaq baza

Ən sadə yol — **bir kompüterdə server, digərində brauzer**:

1. Server olan kompüterdə `.env`-də `HOST=0.0.0.0` yazın.
2. `ipconfig getifaddr en0` (macOS) və ya `ip a` (Linux) ilə lokal IP-ni öyrənin.
3. `python app.py` işlədin, firewall soruşsa **Allow**.
4. İkinci kompüterdə brauzerdə açın: `http://<IP>:5001`

Beləliklə iki maşın eyni bazanı görür (baza yalnız serverdə saxlanılır).

> ⚠️ SQLite faylını Dropbox/iCloud/şəbəkə diski ilə paylaşmayın — file locking düzgün işləmir, baza korrupt ola bilər. Ciddi paralel istifadə üçün PostgreSQL-ə keçin (`DATABASE_URL=postgresql://...`).

## Test datasını sıfırlamaq

`ehtiyat_hisseleri.db` faylını silin — növbəti işə salınmada yenidən yaradılacaq.

## Təhlükəsizlik qeydləri

Bu tətbiq **daxili şəbəkə üçün** nəzərdə tutulub. Public internetə çıxarılacaqsa mütləq:
- HTTPS (nginx/caddy + reverse proxy)
- Production WSGI server (gunicorn / uWSGI) — `flask run` / `python app.py` yalnız development üçündür
- Güclü `SECRET_KEY` və admin parolu
