import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Project
from apps.logs.mongo_models import LogEntry
# Create your views here.
class TestPackage(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'project_name', openapi.IN_QUERY, description="Filter by project name",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'status_code', openapi.IN_QUERY, description="Filter by status code",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request):
        project_name = request.GET.get('project_name').strip()
        status_code = request.GET.get('status_code')

        if not project_name:
            return Response({"error": "project_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.filter(name__exact = project_name).last()
        if not project:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        query = {"access_key": project.access_key}
        if status_code:
            try:
                query["status_code"] = int(status_code)
            except ValueError:
                return Response({"error": "status_code must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        logs = LogEntry.objects(__raw__=query).order_by('-timestamp')[:10]
        response_data = [log.to_mongo().to_dict() for log in logs]
        for log in response_data:
            log['_id'] = str(log['_id'])

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Receive log payload → decrypt → save to MongoDB.
        """
        try:
            request_body = request.data
            log_data = request.data.get('log_data')
            if not request_body:
                return Response({"error": "Missing log_data"}, status=status.HTTP_400_BAD_REQUEST)
            
            project = Project.objects.filter(access_key=request_body.get('access_key')).last()
            
            encryption_key = project.encryption_key

            decrypted_data = decrypt_payload(log_data,encryption_key)

            log_data = decrypted_data.get("log_data")
            access_key = decrypted_data.get("access_key")

            # Merge access_key into log_data
            log_data["access_key"] = access_key
            # Save to MongoDB
            log_entry = LogEntry(**decrypted_data.get("log_data"))
            log_entry.save()

            print("Log stored in MongoDB")
            return Response({"message": "Log saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error storing log:", str(e))
            return Response({"error": "Failed to save log", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

def decrypt_payload(encrypted_payload,encryption_key):
    # Decode the base64 key and validate size
    key = base64.b64decode(encryption_key)

    # Validate key size (16, 24, or 32 bytes)
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid AES key size. Must be 16, 24, or 32 bytes.")

    # Decode from base64
    encrypted_data = base64.b64decode(encrypted_payload)

    # Extract IV (first 16 bytes) and encrypted content
    iv = encrypted_data[:16]
    encrypted_content = encrypted_data[16:]

    # Create cipher and decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_content) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Convert bytes back to JSON
    return json.loads(data.decode('utf-8'))

