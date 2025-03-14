from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DisasterReport
from .forms import DisasterReportForm
import folium

@csrf_exempt
def report_disaster(request):
    """Handles disaster report submissions via standard form submission without CSRF."""
    if request.method == "POST":
        print(" Received POST Data:", request.POST)  # Debugging output
        print(" Received FILES Data:", request.FILES)  # Debugging output
        
        form = DisasterReportForm(request.POST, request.FILES)

        if form.is_valid():
            saved_report = form.save()
            print(" Disaster report saved:", saved_report)  # Debugging confirmation
            return JsonResponse({"success": True, "message": "Disaster reported successfully!"}, status=201)
        else:
            print(" Form Errors:", form.errors)  # Debugging output
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = DisasterReportForm()
    
    return render(request, "disasters/report.html", {"form": form})

def disaster_map(request):
    """Displays real-time disaster reports on a map."""
    reports = DisasterReport.objects.all()

    # Initialize Folium map (Default Center Location)
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add markers for disasters
    for report in reports:
        folium.Marker(
            location=[report.latitude, report.longitude],
            popup=f"{report.disaster_type} ({report.severity}): {report.description}",
            icon=folium.Icon(color="red" if report.severity in ["High", "Critical"] else "blue")
        ).add_to(m)

    map_html = m._repr_html_()
    return render(request, "disasters/map.html", {"map_html": map_html})

def get_disaster_reports(request):
    """Returns disaster reports as JSON for real-time updates."""
    reports = list(DisasterReport.objects.values("disaster_type", "severity", "description", "latitude", "longitude", "timestamp"))
    return JsonResponse(reports, safe=False)