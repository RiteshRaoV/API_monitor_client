import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class TestPackage(APIView):
    def get(self,request):
        return Response({"message":"success!!"},status=status.HTTP_200_OK)
    def post(self,request):
        request_body = request.data.get("log_data")
        request_body = decrypt_payload(request_body)
        response_body = {
            json.dumps(request_body)
        }
        print(response_body)
        return Response(response_body,status=status.HTTP_200_OK)
    
    
    
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

