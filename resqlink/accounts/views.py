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

#this methode is not currently being used
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
def login_register_view(request):
    """
    A single view for both login (front side of card) and register (back side).
    """
    if request.method == 'GET':
        # Render our flip card template
        return render(request, 'accounts/login.html')

    # request.method == 'POST'
    form_type = request.POST.get('form_type')  # "login" or "register"

    if form_type == 'login':
        username = request.POST.get('username')         # or 'login_username'
        password = request.POST.get('password')      # or 'login_password'
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'accounts/home.html')  # or wherever you want
        else:
            # Return the same template with an error message
            return render(request, 'accounts/login.html', {
                'login_error': "Invalid login credentials. Please try again."
            })

    elif form_type == 'register':
        # Gather data for the RegistrationSerializer
        data = {
            'username': request.POST.get('username'),    # Or separate field if you prefer
            'email': request.POST.get('email'),       # same as above or a different field
            'password': request.POST.get('password'),
            'user_type': request.POST.get('user_type', 'normal'),  # e.g. "hospital", "paid"
        }
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # Optionally, auto-login:
            # login(request, user)
            return render(request, 'accounts/login.html', {
                'reg_success': "Registration successful! Please login."
            })
        else:
            print(serializer.errors)
            return render(request, 'accounts/login.html', {
                'reg_errors': serializer.errors
                 
            })

    # If form_type is missing or something else
    print("something went wrong")
    return render(request, 'accounts/login.html')


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
