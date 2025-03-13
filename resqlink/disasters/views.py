from django.shortcuts import render, redirect
from .models import DisasterReport
from .forms import DisasterReportForm
import folium
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DisasterReportSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def report_disaster(request):
    """Allows users to submit disaster reports."""
    if request.method == "POST":
        form = DisasterReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('disaster_map')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = DisasterReportForm()
    
    return render(request, "disasters/report.html", {"form": form})


def disaster_map(request):
    """Displays a real-time crisis map with reported disasters."""
    reports = DisasterReport.objects.all()
    
    # Initialize Folium map (Default Center Location)
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add disaster reports as markers on the map
    for report in reports:
        folium.Marker(
            location=[report.latitude, report.longitude],
            popup=f"{report.disaster_type} ({report.severity}): {report.description}",
            icon=folium.Icon(color="red" if report.severity in ["High", "Critical"] else "blue")
        ).add_to(m)
    
    # Render the map
    map_html = m._repr_html_()
    return render(request, "disasters/map.html", {"map_html": map_html})


@method_decorator(csrf_exempt, name='dispatch')
class DisasterReportAPI(APIView):
    """API endpoint to get and create disaster reports."""
    def get(self, request, format=None):
        reports = DisasterReport.objects.all()
        serializer = DisasterReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DisasterReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_disaster_reports(request):
    """Returns disaster reports as JSON data for real-time updates."""
    reports = DisasterReport.objects.values("disaster_type", "severity", "description", "latitude", "longitude", "timestamp")
    return JsonResponse(list(reports), safe=False)
