import firebase_admin
from firebase_admin import auth, credentials
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\rithe\\Desktop\\Projects\\api_monitor_client\\apps\\jwt_auth\\auth_utils\\firebase-service-account.json")
    firebase_admin.initialize_app(cred)


class FirebaseAuthHandler:
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            email = decoded_token.get('email')
            if email is None:
                return None

            user, created = User.objects.get_or_create(email=email, defaults={
                "username": email.split('@')[0],
            })

            return user

        except Exception as e:
            print(f"Firebase auth error: {e}")
            return None
        
    def register(self, validated_data):
        from firebase_admin import auth
        try:
            user_record = auth.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                display_name=validated_data['username']
            )

            # You can also sync this user to Django if needed:
            user, created = User.objects.get_or_create(
                email=user_record.email,
                defaults={"username": validated_data['username']}
            )

            return {
                "uid": user_record.uid,
                "email": user_record.email,
                "username": user_record.display_name
            }, None

        except Exception as e:
            return None, str(e)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        handler = FirebaseAuthHandler()
        user = handler.authenticate(request)

        if user is None:
            return None
        return (user, None)
