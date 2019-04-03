import django_heroku
import dj_database_url

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
# del DATABASES['default']['OPTIONS']['sslmode']

# Activate Django-Heroku.
django_heroku.settings(locals())

STATIC_ROOT = os.path.join(BASE_DIR, '../static_root/')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
