from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render , redirect

# Import your DRF serializer for user registration
from .serializers import RegistrationSerializer

# Import any custom permission classes
from .permissions import IsHospitalUser

# If using a custom user model with a user_type field:
CustomUser = get_user_model()


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    GET  -> Render the registration page (accounts/register.html).
    POST -> Process the form submission, create a user (via DRF serializer).
    """
    if request.method == 'GET':
        # Just render an HTML form for registration
        return render(request, 'accounts/register.html')

    # request.method == 'POST'
    # Collect form data from the HTML form fields
    data = {
        'username': request.POST.get('username'),
        'email': request.POST.get('email'),
        'password': request.POST.get('password'),
        'user_type': request.POST.get('user_type', 'normal'),  # default to 'normal'
    }

    # Use your DRF serializer to validate and create the user
    serializer = RegistrationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()  # create the user in DB
        # After a successful registration, you can redirect to login, or wherever you want
        return redirect('login')  # Make sure 'login' is a valid URL name
    else:
        # If errors, re-render the template with the errors context
        return render(request, 'accounts/register.html', {'errors': serializer.errors})


# accounts/views.py (add to the same file)

from django.contrib.auth import authenticate, login, logout

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    GET  -> Render the login page (accounts/login.html).
    POST -> Process login form submission, log in the user if valid.
    """
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    # request.method == 'POST'
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        # Redirect to some "dashboard" or "home" after successful login
        if (user.user_type == "hospital") :
            return render(request, 'accounts/hostpital.html')
        elif (user.user_type == "normal") :
            return render(request, 'accounts/home.html')
        elif (user.user_type == "paid user") :
            return render(request, 'accounts/home.html')
        
    else:
        # If authentication fails, show an error
        error_msg = "Invalid credentials"
        return render(request, 'accounts/login.html', {'error_msg': error_msg})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Log out the currently authenticated user.
    Requires an authenticated session (e.g., SessionAuthentication).
    """
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hospital_dashboard(request):
    """
    Example hospital dashboard endpoint.
    Only accessible if user_type == 'hospital'.
    """
    if request.user.user_type != 'hospital':
        return Response({"error": "Access denied"}, status=403)
    return Response({"message": "Welcome, hospital user!"}, status=200)


@api_view(['GET'])
@permission_classes([IsHospitalUser])
def hospital_only_view(request):
    """
    Another hospital-only endpoint, enforced by the IsHospitalUser permission.
    """
    return Response({"message": "Hospital data here"}, status=200)
