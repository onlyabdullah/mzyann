from .base import *

DEBUG = True

ALLOWED_HOSTS = ['www.mzyann.com', 'mzyann.com', '46.101.239.199', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
    'django.contrib.admin',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ] 
