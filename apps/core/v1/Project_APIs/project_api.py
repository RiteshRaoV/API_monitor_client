from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Project
from apps.core.mongo_models import Endpoint
from apps.core.serializers import ProjectSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class ProjectListCreateAPIView(APIView):
	@swagger_auto_schema(
		tags=["Core"],
		manual_parameters=[
			openapi.Parameter(
				'project_id', openapi.IN_QUERY, description="Filter by project id",
				type=openapi.TYPE_INTEGER,
				required=False
			),
		],
		responses={200: "Retrieved Successfully"},
	)
	def get(self, request):
		try:
			project_id = request.GET.get('project_id')
			
			if project_id is not None:
				project = Project.objects.filter(id=project_id).last()
				if project is None:
					return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
				serializer = ProjectSerializer(project)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				projects = Project.objects.all()
				if not projects.exists():
					return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
				serializer = ProjectSerializer(projects, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
	def post(self, request):
		try:
			serializer = ProjectSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EndpointListView(APIView):

	@swagger_auto_schema(
		tags=["Core"],
		responses={200: "Retrieved Successfully"},
		manual_parameters=[
		openapi.Parameter('project_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
	])
	def get(self, request):
		try:
			project_name = request.GET.get("project_name")
			if not project_name:
				return Response({"error": "Project name is required"}, status=status.HTTP_400_BAD_REQUEST)

			project = Project.objects.get(name__icontains=project_name)

			endpoints = Endpoint.objects(access_key=project.access_key).order_by('-updated_at')
			result = [ep.to_mongo().to_dict() for ep in endpoints]
			for item in result:
				if "_id" in item:
					item["_id"] = str(item["_id"])

			return Response(result, status=status.HTTP_200_OK)
		except Project.DoesNotExist:
			return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			import logging
			logging.error(f"EndpointListView error: {e}")
			return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
