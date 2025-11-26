from django.urls import path
from .api_views import AnalyzeTasksAPIView, SuggestTasksAPIView

urlpatterns = [
    path('analyze/', AnalyzeTasksAPIView.as_view(), name='analyze-tasks'),
    path('suggest/', SuggestTasksAPIView.as_view(), name='suggest-tasks'),
]
