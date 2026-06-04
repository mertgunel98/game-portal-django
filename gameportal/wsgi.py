"""
WSGI config for gameportal project.
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameportal.settings')

# Initialize Django settings and apps
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.db import connection

# Safe Programmatic Startup
# These checks prevent Gunicorn workers from repeating heavy setup commands and timing out.

# 1. Run Migrations & Seeding ONLY if tables do not exist
try:
    tables = connection.introspection.table_names()
    if 'games_game' not in tables:
        print("==> Database tables are missing. Running migrations programmatically...")
        call_command('migrate', interactive=False)
        
        # Seed games immediately after migration if empty
        print("==> Seeding initial games data programmatically...")
        call_command('seed_games', interactive=False)
    else:
        print("==> Database tables already exist. Skipping migrations/seeding.")
except Exception as e:
    print(f"Error checking/migrating database: {e}")

# 2. Run Collectstatic ONLY if staticfiles directory doesn't exist or is empty
try:
    staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
    if not os.path.exists(staticfiles_dir) or not os.listdir(staticfiles_dir):
        print("==> Static files are missing. Running collectstatic programmatically...")
        call_command('collectstatic', interactive=False, clear=True)
    else:
        print("==> Static files already collected. Skipping collectstatic.")
except Exception as e:
    print(f"Error checking/collecting static files: {e}")

application = get_wsgi_application()
