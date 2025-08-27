import datetime
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
            openapi.Parameter(
                'request_method', openapi.IN_QUERY, description="Filter by HTTP request method (GET, POST, etc)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'endpoint', openapi.IN_QUERY, description="Filter by endpoint path",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'time_range', openapi.IN_QUERY, description="Filter by time range (JSON: {start, end} as ISO strings)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort_by', openapi.IN_QUERY, description="Sort by field (timestamp, status_code, latency)",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request):
        project_name = request.GET.get('project_name', '').strip()
        status_code = request.GET.get('status_code')
        request_method = request.GET.get('request_method')
        endpoint = request.GET.get('endpoint')
        time_range = request.data.get('time_range')
        sort_stratergy = request.GET.get('sort_by')

        if not project_name:
            return Response({"error": "project_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.filter(name__exact=project_name).last()
        if not project:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        query = {"access_key": project.access_key}
        if status_code:
            try:
                query["status_code"] = int(status_code)
            except ValueError:
                return Response({"error": "status_code must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        if request_method:
            query["method"] = request_method
        if endpoint:
            query["endpoint"] = endpoint
        if time_range:
            # Expecting time_range as dict: {"start": "...", "end": "...">
            start = time_range.get("start")
            end = time_range.get("end")
            if start and end:
                query["timestamp"] = {"$gte": start, "$lte": end}

        # Sorting
        sort_field = '-timestamp'  # default
        if sort_stratergy:
            if sort_stratergy in ['timestamp', 'status_code', 'latency']:
                sort_field = f'-{sort_stratergy}'

        logs = LogEntry.objects(__raw__=query).order_by(sort_field)[:10]
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
            
            update_endpoint_summary(decrypted_data.get("log_data"), access_key)

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


from apps.core.mongo_models import Endpoint

from mongoengine.errors import DoesNotExist

def update_endpoint_summary(log_data, access_key):
    try:
        query = {"access_key": access_key, "path":log_data["endpoint"],"method":log_data["method"]}
        endpoint = Endpoint.objects(__raw__=query).first()
        
        if endpoint is None:
            raise DoesNotExist

        # Update existing endpoint
        endpoint.total_requests += 1
        if log_data["status_code"] >= 400:
            endpoint.total_failures += 1

        # Recalculate averages
        endpoint.average_latency = round(
            (endpoint.average_latency * (endpoint.total_requests - 1) + log_data["latency"]) / endpoint.total_requests, 2
        )
        endpoint.average_db_time = round(
            (endpoint.average_db_time * (endpoint.total_requests - 1) + log_data["db_execution_time"]) / endpoint.total_requests, 2
        )
        endpoint.last_status_code = log_data["status_code"]
        endpoint.updated_at = datetime.datetime.utcnow()
        endpoint.save()

    except DoesNotExist:
        # Create new entry
        endpoint = Endpoint(
            access_key=access_key,
            path=log_data["endpoint"],
            method=log_data["method"],
            app_name=log_data.get("app_name", ""),
            last_status_code=log_data["status_code"],
            average_latency=log_data["latency"],
            average_db_time=log_data["db_execution_time"],
            total_requests=1,
            total_failures=1 if log_data["status_code"] >= 400 else 0,
            tags={"tags": log_data.get("tags", [])}
        )
        endpoint.save()
    except Exception as e:
        print("Error updating endpoint summary:", e)

