from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.templatetags.static import static

# Create your views here.

def register(request):
    """ This helps in displaying the registration page """
    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        username = request.POST['Username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        # Check if the password is at least 8 characters long
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
        # Check if username or email already exists
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use, use another email instead')
        else:
            # Create the user if validation passes
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('accounts_app:login')

    return render(request, 'accounts/register.html')

def login_view(request):
    """ The function helps in displaying the login page """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check whether the user exists in the database
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_superuser and len(password) < 8:
                    messages.error(request, 'Password must be at least 8 characters long for regular users.')
                else:
                    login(request, user)
                    messages.success(request, "You're in! Enjoy your visit.")
                    return redirect("del_app:home")
            else:
                messages.error(request, "Login failed. Incorrect password.")
        else:
            messages.error(request, "No account found with the provided username. Please register.")
            return redirect('accounts_app:register')

    return render(request, 'accounts/login.html')

def logout_view(request):
    """ This is for the logout view"""
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('del_app:home')

def user_profile(request):
    if request.method == 'GET':
        try:
            user_profile = request.user.userprofile
            profile_picture_url = user_profile.profile_picture.url if user_profile.profile_picture and user_profile.profile_picture.name else static('images/default_profile_picture.png')

            context = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'date_of_birth': user_profile.date_of_birth,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'profile_picture': profile_picture_url,
            }
            return render(request, 'accounts/user_profile.html', context)
        except UserProfile.DoesNotExist:
            context = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
                'email': request.user.email,
                'phone': '',
                'date_of_birth': '',
                'location': '',
                'profile_picture': static('images/default_profile_picture.png')
            }
            return render(request, 'accounts/user_profile.html', context)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone = phone

        if date_of_birth:
            try:
                user_profile.date_of_birth = date_of_birth
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
        else:
            user_profile.date_of_birth = None

        user_profile.location = location

        if profile_picture:
            user_profile.profile_picture = profile_picture

        user.save()
        user_profile.save()

        messages.success(request, 'Profile updated successfully' if not created else 'Profile created successfully')
        return redirect('accounts_app:user_profile')

    return render(request, 'accounts/user_profile.html')

def Terms(request):
    """ The function Helps in displaying the terms and conditions page """
    return render(request, 'accounts/terms.html')
