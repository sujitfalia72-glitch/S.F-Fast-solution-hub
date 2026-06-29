from gevent import monkey
monkey.patch_all()

import os

from dotenv import load_dotenv
load_dotenv()

from flask import (
    Flask,
    render_template
)
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from sqlalchemy import text

import cloudinary

from config import Config
from extensions import (
    db,
    socketio,
    limiter
)

# ================= MODELS =================
from models.user import User
from models.chat import Chat
from models.work_model import Work
from models.work_application import WorkApplication
from models.notification import Notification

# ================= ROUTES =================
# ================= ROUTES =================

print("Loading routes.auth")
from routes.auth import auth

print("Loading routes.owner")
from routes.owner import owner

print("Loading routes.admin")
from routes.admin import admin_bp

print("Loading routes.super_admin")
from routes.super_admin import super_admin

print("Loading routes.user")
from routes.user import user

print("Loading routes.main")
from routes.main import main

print("Loading routes.work_routes")
from routes.work_routes import work

print("Loading routes.notification")
from routes.notification import notification_bp

print("Loading routes.live_media")
from routes.live_media import live_media_bp

print("Loading routes.booking")
from routes.booking import booking

print("Loading routes.profile")
from routes.profile import profile_bp


print("Before routes.profile")
from routes.profile import profile_bp
print("After routes.profile")

print("Loading routes.application_routes")
from routes.application_routes import application_bp

print("Loading routes.verification")
from routes.verification import verification

print("Loading routes.chamber.chamber")
from routes.chamber.chamber import chamber_panel

print("Loading routes.chamber.auth")
from routes.chamber.auth import chamber

print("Loading routes.admin_panel.chambers")
from routes.admin_panel.chambers import admin_chambers

print("Loading routes.doctor")
from routes.doctor import doctor_bp

print("✅ All route imports completed")
# ==================================================
# LOGIN MANAGER
# ==================================================
login_manager = LoginManager()
login_manager.login_view = "auth.login"

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )
    
# ==================================================
# DATABASE FIX FUNCTION
# ==================================================
def fix_db(app):

    with app.app_context():
        try:
            pass

            # Example:
            # db.session.execute(
            #     text("UPDATE users SET status='active'")
            # )
            # db.session.commit()

        except Exception as e:
            print(
                f"DB Fix Error: {e}"
)

# ==================================================
# APP FACTORY
# ==================================================
def create_app():
    app = Flask(__name__)

    # ================= CONFIG =================
    app.config.from_object(Config)

    app.secret_key = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    app.config["MAX_CONTENT_LENGTH"] = (
        5 * 1024 * 1024
    )  # 5MB

    # ================= CSRF =================
    csrf.init_app(app)

    # ================= DATABASE =================
    db.init_app(app)

    # ================= LIMITER =================
    limiter.init_app(app)

    # ================= LOGIN =================
    login_manager.init_app(app)

    # ================= SOCKET.IO =================
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="gevent"
    )

    # ================= MIGRATE =================
    Migrate(app, db)

    # ================= CLOUDINARY =================
    cloudinary.config(
        cloud_name=os.getenv(
            "CLOUDINARY_CLOUD_NAME"
        ),
        api_key=os.getenv(
            "CLOUDINARY_API_KEY"
        ),
        api_secret=os.getenv(
            "CLOUDINARY_API_SECRET"
        ),
        secure=True
    )

    # ==================================================
    # REGISTER BLUEPRINTS
    # ==================================================
    blueprints = [
        auth,
        owner,
        admin_bp,
        super_admin,
        user,
        main,
        work,
        booking,
        profile_bp,
        owner_tools,
        application_bp,
        notification_bp,
        live_media_bp,
        verification,
        chamber_panel,
        admin_chambers,
        chamber,
        doctor_bp
    ]

    for bp in blueprints:
        app.register_blueprint(bp)
        
    # ==================================================
    # ERROR HANDLERS
    # ==================================================

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "errors/404.html"
        ), 404


    @app.errorhandler(403)
    def forbidden(error):

        return render_template(
            "errors/403.html"
        ), 403


    @app.errorhandler(500)
    def internal_server_error(error):

        db.session.rollback()

        return render_template(
            "errors/500.html"
        ), 500
    # ==================================================
    # SECURITY HEADERS
    # ==================================================
    # ==================================================
    # SECURITY HEADERS
    # ==================================================
    @app.after_request
    def security_headers(response):

        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https: data:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.socket.io; "
            "connect-src 'self' ws: wss:;"
        )

        return response

    return app
# ==================================================
# CREATE APP
# ==================================================
# ==================================================
# CREATE APP
# ==================================================
import traceback

try:
    app = create_app()
except Exception:
    traceback.print_exc()
    raise

# ==================================================
# DATABASE INIT
# ==================================================
with app.app_context():
    db.create_all()
    fix_db(app)


# ==================================================
# RUN SERVER
# ==================================================
if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
