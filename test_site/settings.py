import os
from django.conf.global_settings import *
from django_extensions.management.commands.generate_secret_key import get_random_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_random_secret_key()
NODE_ENV = os.environ.get('NODE_ENV', 'production')
DEBUG = bool(NODE_ENV == 'development')

ALLOWED_HOSTS = [
    'portal.mpcontribs.org', 'contribs.materialsproject.org', 'localhost',
    'jupyterhub.materialsproject.org', '127.0.0.1', '127.0.0.2', '0.0.0.0', 'docker.for.mac.localhost'
]
ALLOWED_HOSTS += ['10.0.{}.{}'.format(i,j) for i in [10, 11] for j in range(256)]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_extensions',
    'webpack_loader',
    'webtzite',
    'mpcontribs.portal',
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'test_site.urls'

from mpcontribs import users as mpcontribs_users
from glob import glob
path_glob = os.path.abspath(os.path.join(
    os.path.dirname(mpcontribs_users.__file__), '*', 'explorer', 'templates'
))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': glob(path_glob),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'test_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

JPY_USER = os.environ.get('JPY_USER')
PROXY_URL_PREFIX = '/flaskproxy/{}'.format(JPY_USER) if JPY_USER else ''
STATIC_URL = PROXY_URL_PREFIX + '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'dist'),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': './',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

WHITENOISE_KEEP_ONLY_HASHED_FILES = True
APPEND_SLASH = False
