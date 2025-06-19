from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Project
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
