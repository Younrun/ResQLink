from django.urls import path
from .views import report_disaster, disaster_map
from .api_views import DisasterReportAPI

urlpatterns = [
    path('report/', report_disaster, name='report_disaster'),
    path('map/', disaster_map, name='disaster_map'),
    path('api/disaster-reports/', DisasterReportAPI.as_view(), name='api_disaster_reports'),
]
