from django.urls import path
from .api_views import DisasterReportListCreate

urlpatterns = [
    path('api/reports/', DisasterReportListCreate.as_view(), name='api-reports'),
]
