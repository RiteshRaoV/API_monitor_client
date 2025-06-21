from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Project
from apps.core.mongo_models import Endpoint
from apps.core.serializers import ProjectSerializer

from drf_yasg.utils import swagger_auto_schema

class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Project"],
        request_body=ProjectSerializer,
        responses={201: "Created Successfully"},
    )
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from drf_yasg import openapi

class EndpointListView(APIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('project_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    ])
    def get(self, request):
        project_name = request.GET.get("project_name")
        project = Project.objects.filter(name__icontains=project_name).last()
        if not project:
            return Response({"error": "Project not found"}, status=404)

        endpoints = Endpoint.objects(access_key=project.secret_key).order_by('-updated_at')
        result = [ep.to_mongo().to_dict() for ep in endpoints]
        for item in result:
            item["_id"] = str(item["_id"])

        return Response(result, status=200)
