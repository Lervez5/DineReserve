from django.urls import path
from .import views

app_name = 'del_app'

urlpatterns = [
    path('',views.home,name='home'),# Home section 
    path('about/',views.about,name='about'),# About section 
    path('menu/',views.menu,name='menu'),# Menu section 
    path('events/',views.events,name='events'),# Events section
    path('gallery/',views.gallery,name='gallery'),# Gallery section 
    path('contact/',views.contact,name='contact'),# For the contact section
    path('show_contacts/',views.contact_info, name="show_contacts"), # For contact information
    path('edit_contact/<int:contact_id>/', views.update_contact, name='update_contact'), # For any contact information edits
    path('delete_contact/<int:id>/', views.delete_contact, name='delete_contact'), # For any details that entai contact info deletions
    path('book_table/',views.booking_table, name="book_table"), # For Table bookings
    path('show_bookings/', views.show_bookings, name="show_bookings"), # For showing Bookings update
    path('delete/<int:id>/', views.delete_booking, name= 'delete_booking'), # For any booking deletions
    path('edit/<int:booking_id>/', views.update_booking, name="edit_booking"), # For any Booking updates

    # Urls used in togetherness with the mpesa api
    path('pay/', views.pay, name='pay'), # The view for the payment form
    path('stk/', views.stk, name='stk'), # Its function is to send the stk push prompt
    path('token/', views.token, name='token'), # generates a token for any particular transaction that takes place
]
