"""Application entry point.

`python app.py` layihəni işə salır. Konfiqurasiya .env faylından oxunur.
"""
import os

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.seed import seed_if_empty

load_dotenv()

app = create_app()


@app.cli.command("seed")
def seed_command():
    """Test datasını bazaya yükləyir (əgər boşdursa)."""
    with app.app_context():
        seed_if_empty()
        print("Seed tamamlandı.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_if_empty()

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5001"))  # macOS 5000-i AirPlay üçün istifadə edir
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
