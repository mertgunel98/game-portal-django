"""
WSGI config for gameportal project.
"""

import os
import django
import time
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameportal.settings')

# Initialize Django settings and apps
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.db import connection

# Safe Multi-Worker Startup Lock
lock_file = os.path.join(settings.BASE_DIR, 'startup.lock')

# If lock file exists, another worker is doing the setup. Wait for it to finish (max 60s).
if os.path.exists(lock_file):
    print("==> Another worker is performing startup tasks. Waiting...")
    start_time = time.time()
    while os.path.exists(lock_file) and (time.time() - start_time) < 60:
        time.sleep(1)

# Double check if we need to do the setup
try:
    tables = connection.introspection.table_names()
    db_needs_migration = 'games_game' not in tables
except Exception as e:
    print(f"Error checking database: {e}")
    db_needs_migration = True

staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
static_needs_collection = not os.path.exists(staticfiles_dir) or not os.listdir(staticfiles_dir)

# Run setup if needed and we can acquire the lock
if (db_needs_migration or static_needs_collection) and not os.path.exists(lock_file):
    try:
        # Acquire lock
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # 1. Run migrations if tables are missing
        if db_needs_migration:
            try:
                print("==> Database tables are missing. Running migrations programmatically...")
                call_command('migrate', interactive=False)
            except Exception as e:
                print(f"Error during migrate: {e}")
            
            # Seed games immediately if we just migrated
            try:
                from games.models import Game
                if Game.objects.count() == 0:
                    print("==> Database is empty. Seeding games programmatically...")
                    call_command('seed_games')
            except Exception as e:
                print(f"Error during seeding: {e}")
        
        # 2. Run collectstatic if staticfiles is missing
        if static_needs_collection:
            try:
                print("==> Static files are missing. Running collectstatic programmatically...")
                call_command('collectstatic', interactive=False, clear=True)
            except Exception as e:
                print(f"Error during collectstatic: {e}")
            
    except Exception as e:
        print(f"Error during startup setup: {e}")
    finally:
        # Release lock
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print("==> Startup setup completed and lock released.")
        except Exception as e:
            print(f"Error releasing lock: {e}")

# If we have tables but no games (in case migrations ran but seeding failed or was skipped)
try:
    tables = connection.introspection.table_names()
    if 'games_game' in tables:
        from games.models import Game
        if Game.objects.count() == 0:
            print("==> Database has no games. Seeding games programmatically...")
            call_command('seed_games')
except Exception as e:
    print(f"Error checking/seeding games: {e}")

application = get_wsgi_application()
