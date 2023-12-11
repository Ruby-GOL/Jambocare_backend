import os

from django.core.wsgi import get_wsgi_application

settings_module = 'backend.production' if 'PRODUCTION' in os.environ else 'backend.settings'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
