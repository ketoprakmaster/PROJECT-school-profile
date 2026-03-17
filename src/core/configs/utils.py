import sys
import os

def summarize_services(var: dict):
    """
    Prints a summary of active services.
    Pass 'settings' as the argument from the settings file.
    """
    # Only print during interactive commands
    interactive_cmds = ['runserver', 'migrate', 'collectstatic']
    if not any(arg in sys.argv for arg in interactive_cmds):
        return


    print("\n" + "─" * 50)
    print(f" 🛠️  CONFIG LOADED   : {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print("─" * 50)

    # Database
    DATABASES = var.get("DATABASES", {})
    db = DATABASES.get("default", {})
    engine = db.get('ENGINE', 'N/A').split('.')[-1]
    name = db.get('NAME', 'N/A')
    host = db.get('HOST', 'localhost')
    print(f" 🔹 DB ENGINE        : {engine}")
    print(f" 🔹 DB TARGET        : {host} / {name}")

    # Storages
    STORAGES = var.get("STORAGES", {})
    static_backend = STORAGES['staticfiles']['BACKEND'].split('.')[-1]
    media_backend = STORAGES['default']['BACKEND'].split('.')[-1]
    print(f" 🔹 STORAGE (Static) : {static_backend}")
    print(f" 🔹 STORAGE (Media)  : {media_backend}")

    # Email
    EMAIL_BACKEND = var.get("EMAIL_BACKEND", {})
    email = EMAIL_BACKEND.split('.')[-1]
    print(f" 🔹 EMAIL            : {email}")

    # Logging / Sentry
    from core.configs.logs import SENTRY_DSN
    sentry_status = "✅ ACTIVE" if SENTRY_DSN else "❌ DISABLED"
    print(f" 🔹 SENTRY           : {sentry_status}")

    # Debug Status
    debug_status = "⚠️ ON" if var.get("DEBUG") else "✅ OFF"
    environment = var.get("ENVIRONMENT")
    log_status = var.get("LOG_LEVEL")
    print(f" 🔹 DEBUG MODE       : {debug_status}")
    print(f" 🔹 ENVIRONMENT      : {environment}")
    print(f" 🔹 LOG LEVEL        : {log_status}")
    print("─" * 50 + "\n")
