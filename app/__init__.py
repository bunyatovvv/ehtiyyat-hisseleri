"""Flask application factory."""
import os

from flask import Flask

from .extensions import db, login_manager, csrf
from .models import AdminUser


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # --- Konfiqurasiya ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///ehtiyat_hisseleri.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "admin.login"
    login_manager.login_message = "Bu səhifəyə giriş üçün daxil olun."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(AdminUser, int(user_id))

    # --- Blueprints ---
    from .routes.public import public_bp
    from .routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
