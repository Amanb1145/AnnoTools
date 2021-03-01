from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .annotation_tool import return_annotated_file
from .models import AnnoTool
from .serializer import AnnoSerializer

class anno_tool(APIView):

    def get(self, request):
        file = AnnoTool.objects.filter(resume=request.GET.get("resume"))
        fileserializer = AnnoSerializer(file)
        print(fileserializer.data)
        name = AnnoTool.objects.filter(name=request.GET.get("name"))
        #name = AnnoSerializer(namei)
        degree = AnnoTool.objects.filter(degree=request.GET.get("degree"))
        #degree = AnnoSerializer(degreei)
        college = AnnoTool.objects.filter(college=request.GET.get("college"))
        #college = AnnoSerializer(collegei)
        organization = AnnoTool.objects.filter(organization=request.GET.get("organization"))
        #organization = AnnoSerializer(organizationi)
        designation = AnnoTool.objects.filter(designation=request.GET.get("designation"))
        #designation = AnnoSerializer(designationi)
        date_of_birth = AnnoTool.objects.filter(date_of_birth=request.GET.get("date_of_birth"))
        #date_of_birth = AnnoSerializer(date_of_birthi)
        summary = AnnoTool.objects.filter(summary=request.GET.get("summary"))
        #summary = AnnoSerializer(summaryi)
        ents = [name, degree, college, organization, designation, date_of_birth, summary]
        return return_annotated_file(file, ents)



