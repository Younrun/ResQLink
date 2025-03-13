from django import forms
from .models import DisasterReport

class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ['disaster_type', 'severity', 'description', 'latitude', 'longitude', 'image']
        widgets = {
            'disaster_type': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
