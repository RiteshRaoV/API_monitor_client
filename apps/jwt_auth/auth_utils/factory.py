# apps/jwt_auth/auth_utils/factory.py

from django.conf import settings
from .jwt_auth import JWTAuthHandler
from .firebase_auth import FirebaseAuthHandler 

def get_auth_handler():
    provider = getattr(settings, "AUTH_PROVIDER", "JWT").upper()

    if provider == "JWT":
        return JWTAuthHandler()

    elif provider == "FIREBASE":
        return FirebaseAuthHandler()

    else:
        raise ValueError(f"Unsupported AUTH_PROVIDER: {provider}")
