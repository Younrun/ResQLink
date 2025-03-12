# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('paid', 'Paid User'),
        ('hospital', 'Hospital'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
            user_type=data['user_type'],
        )
        return user
