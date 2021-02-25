from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .annotation_tool import return_annotated_file

class anno_tool(APIView):

    def post(self, requests):
        file = requests.data.get("file", None)
        ents = requests.data.get["ents"]
        return return_annotated_file(file, ents)


