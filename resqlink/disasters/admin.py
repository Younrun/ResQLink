from django.contrib import admin

from django.contrib import admin
from .models import DisasterReport

@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ('disaster_type', 'severity', 'user', 'latitude', 'longitude', 'timestamp')
    list_filter = ('disaster_type', 'severity', 'timestamp')
    search_fields = ('disaster_type', 'user__username', 'description')
    ordering = ('-timestamp',)  # Show latest reports first

