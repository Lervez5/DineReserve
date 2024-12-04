from django.urls import path
from . import views

app_name = 'accounts_app'

urlpatterns = [
    path('register/', views.register, name="register"), # register
    path('login/', views.login_view, name="login"), # login
    path('logout/', views.logout_view, name='logout'), # Logout
    path('user/', views.user_profile, name='user_profile'), # For user_profiles
    path('Terms/', views.Terms, name="Terms"), # Terms and conditions
]
