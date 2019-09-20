import sys
from os import getenv
from dotenv import load_dotenv
from .base import *

load_dotenv()

DEBUG = True

STRIPE_API_KEY = getenv("STRIPE_API_KEY")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv("DB_NAME", "turing_db"),
        "USER": getenv("DB_USER", "root"),
        "PASSWORD": getenv("DB_PASSWORD", ""),
        "HOST": getenv("DB_HOST", "localhost"),
        "PORT": getenv("DB_PORT", "3306"),
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
