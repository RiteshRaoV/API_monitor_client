import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.logs.mongo_models import LogEntry
# Create your views here.
class TestPackage(APIView):
    def get(self, request):
        """
        Fetch recent logs from MongoDB (limit to 10 for example).
        """
        logs = LogEntry.objects.order_by('-timestamp')[:10]
        response_data = [log.to_mongo().to_dict() for log in logs]
        for log in response_data:
            log['_id'] = str(log['_id'])  # Convert ObjectId to str for JSON
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Receive log payload → decrypt → save to MongoDB.
        """
        try:
            request_body = request.data.get("log_data")
            if not request_body:
                return Response({"error": "Missing log_data"}, status=status.HTTP_400_BAD_REQUEST)

            decrypted_data = decrypt_payload(request_body)

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

def decrypt_payload(encrypted_payload):
    # Decode the base64 key and validate size
    key = base64.b64decode("nxyS44dXrJPK1BG++M6Rjxqtu5g0fLpi5xLLnwNVpB0=")

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

