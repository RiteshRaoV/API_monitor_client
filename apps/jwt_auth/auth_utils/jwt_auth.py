from .base import BaseAuthHandler
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthHandler(BaseAuthHandler):
    def register(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if User.objects.filter(email=email).exists():
            return None, "Email already in use"
        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, None

    def login(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, None
            return None, "Invalid credentials"
        except User.DoesNotExist:
            return None, "User does not exist"


    def validate_token(self, token):
        auth = JWTAuthentication()
        validated_token = auth.get_validated_token(token)
        return auth.get_user(validated_token)

    def get_user(self, token):
        return self.validate_token(token)
