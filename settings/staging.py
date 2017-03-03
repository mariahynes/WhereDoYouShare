from base import *
import dj_database_url
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES['default'] = dj_database_url.parse("mysql://b2d4afa033676f:96718e38@eu-cdbr-west-01.cleardb.com/heroku_50808dd0056e876")

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_uO9j8R0OdPOhbUzwSI4VTevH')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_D3WTWnQ99nHuosPRBfpnpSSs')