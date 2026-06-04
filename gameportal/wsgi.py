"""
WSGI config for gameportal project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameportal.settings')

# Orijinal temiz wsgi.py - kilitlenmeleri önlemek için veritabanı işlemlerini burada yapmıyoruz.
application = get_wsgi_application()
