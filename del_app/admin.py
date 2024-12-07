from django.contrib import admin
from .models import contacts,booking,MenuItem,Gallery,Testimonial

# Register your models here.
admin.site.register(contacts)
admin.site.register(booking)
admin.site.register(MenuItem)
admin.site.register(Gallery)
admin.site.register(Testimonial)
