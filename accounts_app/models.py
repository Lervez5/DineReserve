from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True,null=True)

    # Returns values to human readable format
    def __str__(self):
        return f"{self.user.username} Profile"        