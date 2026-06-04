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

# 1. Run Migrations
try:
    print("==> Running migrations programmatically...")
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Error running migrate: {e}")

# 2. Run Collectstatic if staticfiles directory doesn't exist or is empty
staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
if not os.path.exists(staticfiles_dir) or not os.listdir(staticfiles_dir):
    try:
        print("==> Running collectstatic programmatically...")
        call_command('collectstatic', interactive=False, clear=True)
    except Exception as e:
        print(f"Error running collectstatic: {e}")

# 3. Seed Games only if database is empty to prevent wiping user data on worker restarts
try:
    from games.models import Game
    if Game.objects.count() == 0:
        print("==> Database is empty. Seeding games programmatically...")
        call_command('seed_games', interactive=False)
    else:
        print(f"==> Database already has {Game.objects.count()} games. Skipping seed.")
except Exception as e:
    print(f"Error checking/seeding games: {e}")

application = get_wsgi_application()
