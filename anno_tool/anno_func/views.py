from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .annotation_tool import return_annotated_file
from .models import AnnoTool
from .serializer import AnnoSerializer

class anno_tool(APIView):

    def get(self, request):
        data = {
            "resume": AnnoTool.objects.filter(resume=request.GET.get("resume")),
            "name": AnnoTool.objects.filter(name=request.GET.get("name")),
            "degree": AnnoTool.objects.filter(degree=request.GET.get("degree")),
            "college": AnnoTool.objects.filter(college=request.GET.get("college")),
            "organization": AnnoTool.objects.filter(organization=request.GET.get("organization")),
            "designation": AnnoTool.objects.filter(designation=request.GET.get("designation")),
            "date_of_birth": AnnoTool.objects.filter(date_of_birth=request.GET.get("date_of_birth")),
            "summary": AnnoTool.objects.filter(summary=request.GET.get("summary"))
        }
        dataserializer = AnnoSerializer(data)

        return return_annotated_file(data.get("resume"), dict(list(data.items())[1:]))



