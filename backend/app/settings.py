import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Add your app here
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure this line is present
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app' / 'templates'],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Remove STRIPE settings and add PayPal settings
PAYPAL_CLIENT_ID = 'AY4CZZ1hhyDwYszHx-h28orO9RaGscf1qScWiePW-R-C3LsXKYSl6O-2oe-SMK5Rl6aVbcE4zqWi-00C'
PAYPAL_CLIENT_SECRET = 'EJQUhBNU8bfy9okZtU39HFpUO97QHt-OyJ8fRJOAC1_UbR-ukeFyxH0Yr6YXM96fgEN9S2pKSI0umQU0'
PAYPAL_SANDBOX = True  # Set to False in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your allowed hosts here

# Ensure DEBUG is set to True for development
DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://www.sandbox.paypal.com',
    'https://www.paypal.com',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
]

# Add REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'