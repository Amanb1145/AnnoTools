from django.urls import path, include
from .views import anno_tool

urlpatterns = [
    path('caption/', anno_tool.as_view())
]