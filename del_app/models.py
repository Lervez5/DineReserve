from django.db import models

# Create your models here.
class booking(models.Model):
    """ bookings table """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    people = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)

    # Returns the values to human readable format    
    def __str__(self):
        return f"booking by {self.name} at {self.time} - {self.date}"

class contacts(models.Model):
    """ Contacts table """
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    # Returns the values to human readable format    
    def __str__(self):
        return self.name
