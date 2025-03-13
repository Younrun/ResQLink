from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DisasterReport
from .serializers import DisasterReportSerializer

class DisasterReportAPI(APIView):
    """API endpoint to get disaster reports and create new ones."""

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
