from rest_framework import serializers
from .models import DisasterReport

class DisasterReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterReport
        fields = '__all__'
