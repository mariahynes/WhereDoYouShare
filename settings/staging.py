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

DATABASES['default'] = dj_database_url.config("mysql://b7ab21e69f38ee:5ceb1621@eu-cdbr-west-01.cleardb.com/heroku_a101d16357a9fdc?reconnect=true")

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_uO9j8R0OdPOhbUzwSI4VTevH')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_D3WTWnQ99nHuosPRBfpnpSSs')