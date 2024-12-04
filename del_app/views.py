import json
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from del_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import contacts, booking

def home(request):
    """ This is for the home_page """
    return render(request, 'index.html')

def about(request):
    """ This is for the about page """
    return render(request, 'about.html')

def menu(request):
    """ This is for the menu page """
    return render(request, 'menu.html')

def events(request):
    """ This is for the events page """
    return render(request, 'events.html')

def gallery(request):
    """ This is for the Gallery page """
    return render(request, 'gallery.html')

@login_required(login_url='accounts_app:login')
def contact(request):
    """ This is for the contact section page """
    if request.method == 'POST':
        # Creates a variable to pick the input fields
        contact_instance = contacts(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        # Save's the variables
        contact_instance.save()
        # Redirect to home page after saving
        return redirect('del_app:home')
    else:
        # Render's the contact page if its a GET request
        return render(request, 'contact.html')

def contact_info(request):
    """ Shows the contacts information """
    # Variable to store all contacts
    contact_instance = contacts.objects.all()
    context = {'contacts': contact_instance}
    # Render the show contacts page with the contacts context
    return render(request, 'show_contacts.html', context)

def update_contact(request, contact_id):
    """ Function to update an existing contact """
    # Get the contact object or return 404 if not found
    contact_instance = get_object_or_404(contacts, id=contact_id)
    if request.method == 'POST':
        # Update the contact with the new data from the form
        contact_instance.name = request.POST.get('name')
        contact_instance.email = request.POST.get('email')
        contact_instance.subject = request.POST.get('subject')
        contact_instance.message = request.POST.get('message')
        # Save the updated contact
        contact_instance.save()
        # Redirect to the show contacts page after updating
        return redirect('del_app:show_contacts')
    # Render the update contact page if GET request
    return render(request, "edit_contact.html", {'contact': contact_instance})

def delete_contact(request, id):
    """ Deleting The contacts """
    # Fetch a particular contact by its original id
    contact_instance = get_object_or_404(contacts, id=id)
    # Actual action of deleting
    contact_instance.delete()
    # Redirect to the show contacts page after deleting
    return redirect('del_app:show_contacts')

@login_required(login_url='accounts_app:login')
def booking_table(request):
    """ This is for the Table bookings page """
    if request.method == 'POST':
        # Create a variable to pick the input fields and save the form data
        bookings_instance = booking(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            people=request.POST['people'],
            message=request.POST['message'],
        )
        # Save all the inputs into the Database
        bookings_instance.save()
        # Redirect to home page after saving
        return redirect('del_app:home')
    else:
        # Render the booking table page if GET request
        return render(request, 'book_table.html')

def show_bookings(request):
    """ Shows the bookings information """
    # Variable to store all bookings
    all_bookings = booking.objects.all()
    context = {'bookings': all_bookings}
    # Render the show bookings page with the bookings context
    return render(request, 'show_bookings.html', context)

def update_booking(request, booking_id):
    """ Function to update an existing booking """
    # Get the booking object or return 404 if not found
    bookings_instance = get_object_or_404(booking, id=booking_id)
    if request.method == 'POST':
        # Update the booking with the new data from the form
        bookings_instance.name = request.POST.get('name')
        bookings_instance.email = request.POST.get('email')
        bookings_instance.phone = request.POST.get('phone')
        bookings_instance.date = request.POST.get('date')
        bookings_instance.time = request.POST.get('time')
        bookings_instance.people = request.POST.get('people')
        bookings_instance.message = request.POST.get('message')
        # Save the updated booking
        bookings_instance.save()
        # Redirect to the show bookings page after updating
        return redirect('del_app:show_bookings')
    # Render the update booking page if GET request
    return render(request, "edit_booking.html", {'booking': bookings_instance})

def delete_booking(request, id):
    """ Deleting The bookings """
    # Fetch a particular booking by its original id
    bookings_instance = get_object_or_404(booking, id=id)
    # Actual action of deleting
    bookings_instance.delete()
    # redirects to the show bookings page after any deletion
    return redirect('del_app:show_bookings')


# Adding the mpesa functionality
# Function to Display the payments form
def pay(request):
   """ Renders the Payment form """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = '56TRjogIXUNmAmVrTlAeqmOtjad1o80GfUPQ2gOBSavUBpPO'
    consumer_secret = 'fTXbvpK6eDG1NvnRxG0M5kYqaKaDUoCxvnyVbPMx71LugWb222qOCkcj8MrTIUAS'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Dinereserve Restaurant",
            "TransactionDesc": "Booking Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")