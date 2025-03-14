from django.urls import path
from .views import report_disaster, disaster_map, get_disaster_reports

urlpatterns = [
    path('report/', report_disaster, name='report_disaster'),
    path('map/', disaster_map, name='disaster_map'),
    path('get-disasters/', get_disaster_reports, name='get_disaster_reports'),  # Replaces API
]
