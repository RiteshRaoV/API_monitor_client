
# Create your views here.
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.jwt_auth.auth_utils.firebase_auth import FirebaseAuthHandler
from rest_framework_simplejwt.views import TokenObtainPairView

from .auth_utils.factory import get_auth_handler
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully'),
            400: 'Validation error or email already in use'
        }
    )
    def post(self, request):
        auth_handler = get_auth_handler()
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            response, error = auth_handler.register(serializer.validated_data)
            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    auth_handler = get_auth_handler()
    user = auth_handler.authenticate(request)
    if user:
        return Response({'message': f'Hello {user.username}! Authenticated via {settings.AUTH_PROVIDER}'})
    return Response({'error': 'Authentication failed'}, status=401)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class UnifiedLoginView(APIView):
    def post(self, request):
        # Case 1: Firebase token in headers
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            # Firebase path
            handler = FirebaseAuthHandler()
            user = handler.authenticate(request)
            if user is None:
                return Response({"error": "Invalid Firebase token"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["username"] = user.username
            refresh["is_superuser"] = user.is_superuser

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })

        # Case 2: Regular email/password login
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Missing email or password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["username"] = user.username
        refresh["is_superuser"] = user.is_superuser

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })