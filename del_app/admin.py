from django.contrib import admin
from .models import contacts,booking,MenuItem

# Register your models here.
admin.site.register(contacts),
admin.site.register(booking),
admin.site.register(MenuItem)