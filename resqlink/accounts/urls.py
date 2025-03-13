from django.urls import path
from .views import (
   
    login_register_view,
    logout_user,
    hospital_dashboard,
    hospital_only_view
)

urlpatterns = [
    
    
    path('login/', login_register_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('hospital-dashboard/', hospital_dashboard, name='hospital_dashboard'),
    path('hospital-only-view/', hospital_only_view, name='hospital_only_view'),
]
