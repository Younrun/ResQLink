from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    hospital_dashboard,
    hospital_only_view
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('hospital-dashboard/', hospital_dashboard, name='hospital_dashboard'),
    path('hospital-only-view/', hospital_only_view, name='hospital_only_view'),
]
