# Ehtiyat hissələri

Maşın ehtiyat hissələri satan mağazaları idarə etmək üçün daxili (lokal şəbəkədə istifadə üçün) veb tətbiq. İşçilər avtomobil markasını seçir, uyğun mağazaların siyahısını görür və birbaşa WhatsApp-dan mağazaya yaza bilir. Mağazalar Azərbaycan və Gürcüstanda ola bilər — WhatsApp mesajı avtomatik olaraq mağazanın ölkəsinə uyğun dildə (Azərbaycanca / Gürcücə) hazırlanır.

## Texniki stack

- **Backend:** Python 3.7+, Flask 2.2, Flask-SQLAlchemy, Flask-Login, Flask-WTF (CSRF)
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

## Windows 7 / Windows 8.1 quraşdırma

Tətbiq **Python 3.7-13** arasında bütün versiyalarda işləyir. Windows 7-də ən stabil Python `3.7.9`, Windows 8.1-də isə `3.9.13`-dir.

### Windows 7-də quraşdırma (sadə yol)

1. **Python 3.7.9** endirin: <https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe>
   - Quraşdırarkən **"Add Python 3.7 to PATH"** qutusunu qeyd edin (vacibdir)
   - "Install Now" seçin
2. Layihəni endirin: <https://github.com/bunyatovvv/ehtiyyat-hisseleri>
   - Yaşıl **Code** düyməsi → **Download ZIP**
   - ZIP-i istənilən qovluğa açın (məs: `C:\ehtiyyat-hisseleri`)
3. `start.bat` faylına **iki dəfə klik edin**.
   - İlk dəfə: virtual environment quracaq, asılılıqları install edəcək (2-5 dəqiqə)
   - Sonrakı dəfələr: birbaşa serveri qaldıracaq
4. Brauzerdə açın: <http://127.0.0.1:5001>

Serveri dayandırmaq üçün açılan pəncərədə **Ctrl+C** basın (ya da pəncərəni bağlayın).

### Windows 7-də quraşdırma (əl ilə, `start.bat` işləmirsə)

Command Prompt (Start → cmd yazın):

```cmd
cd C:\ehtiyyat-hisseleri
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python app.py
```

### Windows 8.1-də quraşdırma

Yuxarıdakı ilə **eyni**, sadəcə Python versiyası fərqli:
- Python 3.9.13 endirin: <https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe>

### Windows-a məxsus problemlər

**Problem: `pip install` SSL / TLS xətası verir**
- Windows 7 SP1 quraşdırılmalıdır (Service Pack 1)
- KB3140245 və KB3138612 update-ləri lazım ola bilər (TLS 1.2 dəstəyi üçün)
- Alternativ olaraq:
  ```cmd
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
  ```

**Problem: `python` komandası tapılmır**
- Python-u quraşdırarkən "Add to PATH" seçilməyib
- Həll: Python-u uninstall edib yenidən quraşdırın, bu dəfə checkbox-a diqqət edin

**Problem: Firewall port 5001-i bloklayır (başqa kompüterdən girmək üçün)**
- Windows Firewall → Advanced Settings → Inbound Rules → New Rule → Port → TCP 5001 → Allow

**Qeyd:** Sistem növ zamanı avtomatik başlaması üçün `python app.py`-nı bir `.bat` faylına yerləşdirib `shell:startup` qovluğuna qoya bilərsiniz.

## 2 (və ya daha çox) kompüter arasında ortaq baza

Ən sadə və problemsiz yol — **bir kompüteri "server" edin, digərləri sadəcə brauzerdən qoşulsun**. Baza avtomatik ortaq olur çünki yalnız bir yerdə saxlanılır.

### Windows-da (start.bat istifadə edərək)

**Server kompüterində:**
1. `start.bat`-a iki dəfə klik → server LAN mode-da qalxır
2. Ekranda görəcəksiniz:
   ```
   Bu kompuuterde:
     http://127.0.0.1:5001
   
   Basqa kompuuterden:
     http://192.168.1.15:5001    ← bu IP-ni yaddaşinızda saxlayın
   ```
3. **Windows Firewall pop-up** çıxarsa **"Allow"** basın.
4. İlk dəfə isə **Firewall Inbound Rule** əlavə etmək lazım ola bilər:
   - Start → yazın: `Windows Defender Firewall with Advanced Security`
   - **Inbound Rules** → **New Rule** → **Port** → **TCP** → **Specific local ports: 5001** → **Allow** → Next Next Finish

**Digər kompüterdə** (heç nə install etməyə ehtiyac yoxdur):

Brauzeri açın (Chrome, Edge, hər hansı) və yazın:
```
http://<server-ip>:5001
```
(server-ip yerinə birinci kompüterin ekranındakı IP — məs `http://192.168.1.15:5001`)

Bütün istifadəçilər eyni bazanı görür — baza server kompüterində durur, digərləri onun üzərindən işləyir.

### Vacib qeydlər

- **Server kompüteri yandırılmalıdır** — söndürsəniz digərləri işləyə bilməz. Ona görə həmişə açıq qalacaq kompüteri "server" seçin.
- **IP dəyişməsin deyə** router paneldən statik IP təyin edin (DHCP → Reserved Addresses).
- **VPN / mobile hotspot** işlədirsinizsə, hər iki kompüter **eyni Wi-Fi / şəbəkəyə** qoşulmalıdır.

### ⚠️ Etməyin

**SQLite faylını Dropbox / iCloud / OneDrive / şəbəkə diskində paylaşmayın** — SQLite-ın file locking mexanizmi şəbəkə fayl sistemlərində işləmir, baza tez bir zamanda **korrupt olur**. Rəsmi SQLite sənədləri bunu qəti qadağan edir.

### Ciddi paralel istifadə (opsional, gələcək üçün)

Bir çox istifadəçi eyni anda aktiv yazırsa (məsələn 5+ nəfər eyni zamanda mağaza əlavə edir), SQLite performansı zəifləyə bilər. O zaman PostgreSQL-ə keçmək olar:

1. Bir kompüterdə PostgreSQL install edin (pulsuz, <https://www.postgresql.org/download/windows/>)
2. `.env`-də dəyişin: `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
3. `pip install psycopg2-binary`
4. Kod dəyişikliyi yoxdur — SQLAlchemy driveri özü seçir

## Test datasını sıfırlamaq

`ehtiyat_hisseleri.db` faylını silin — növbəti işə salınmada yenidən yaradılacaq.

## Təhlükəsizlik qeydləri

Bu tətbiq **daxili şəbəkə üçün** nəzərdə tutulub. Public internetə çıxarılacaqsa mütləq:
- HTTPS (nginx/caddy + reverse proxy)
- Production WSGI server (gunicorn / uWSGI) — `flask run` / `python app.py` yalnız development üçündür
- Güclü `SECRET_KEY` və admin parolu
