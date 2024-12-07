import json
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from del_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import contacts, booking, MenuItem, Gallery ,Testimonial

def home(request):
    """ This is for the home_page """
    return render(request, 'index.html')

def about(request):
    """ This is for the about page """
    return render(request, 'about.html')

def menu(request):
    """ This is for the menu view """
    item_to_edit = None

    if request.method == 'POST':
        if 'add_item' in request.POST:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category = request.POST.get('category')
            image = request.FILES.get('image')

            MenuItem.objects.create(name=name, description=description, price=price, category=category, image=image)
            return redirect('del_app:menu')

        if 'edit_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            item.name = request.POST.get('name')
            item.description = request.POST.get('description')
            item.price = request.POST.get('price')
            item.category = request.POST.get('category')
            if request.FILES.get('image'):
                item.image = request.FILES.get('image')
            item.save()
            return redirect('del_app:menu')

        if 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            item.delete()
            return redirect('del_app:menu')

    if 'edit' in request.GET:
        item_to_edit = get_object_or_404(MenuItem, id=request.GET.get('edit'))

    appetizers = MenuItem.objects.filter(category='APPETIZER')
    main_courses = MenuItem.objects.filter(category='MAIN_COURSE')
    desserts = MenuItem.objects.filter(category='DESSERT')
    drinks = MenuItem.objects.filter(category='DRINK')

    context = {
        'appetizers': appetizers,
        'main_courses': main_courses,
        'desserts': desserts,
        'drinks': drinks,
        'item_to_edit': item_to_edit,
    }
    return render(request, 'menu.html', context)

def events(request):
    """ This is for the events page """
    return render(request, 'events.html')

def gallery(request):
    """ This is for the gallery and testimonials view """
    if request.method == 'POST':
        if 'add_image' in request.POST:
            image = request.FILES.get('image')
            caption = request.POST.get('caption')
            if image:  # Ensure an image file is provided
                Gallery.objects.create(image=image, caption=caption)
                messages.success(request, "Image added successfully!")
            else:
                messages.error(request, "Please upload an image.")
            return redirect('del_app:gallery')

        if 'delete_image' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(Gallery, id=image_id)
            image.delete()
            messages.success(request, "Image deleted successfully!")
            return redirect('del_app:gallery')

        if 'add_testimonial' in request.POST:
            name = request.POST.get('name')
            role = request.POST.get('role')
            stars = request.POST.get('stars')
            quote = request.POST.get('quote')
            image = request.FILES.get('image')
            if name and quote:  # Ensure required fields are provided
                Testimonial.objects.create(name=name, role=role, stars=stars, quote=quote, image=image)
                messages.success(request, "Testimonial added successfully!")
            else:
                messages.error(request, "Please provide the required fields.")
            return redirect('del_app:gallery')

        if 'delete_testimonial' in request.POST:
            testimonial_id = request.POST.get('testimonial_id')
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.delete()
            messages.success(request, "Testimonial deleted successfully!")
            return redirect('del_app:gallery')

    images = Gallery.objects.exclude(image='')
    testimonials = Testimonial.objects.all()

    context = {
        'images': images,
        'testimonials': testimonials,
    }
    return render(request, 'gallery.html', context)

@login_required(login_url='accounts_app:login')
def contact(request):
    """ This is for the contact section page """
    if request.method == 'POST':
        contact_instance = contacts(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        contact_instance.save()
        return redirect('del_app:home')
    else:
        return render(request, 'contact.html')

def contact_info(request):
    """ Shows the contacts information """
    contact_instance = contacts.objects.all()
    context = {'contacts': contact_instance}
    return render(request, 'show_contacts.html', context)

def update_contact(request, contact_id):
    """ Function to update an existing contact """
    contact_instance = get_object_or_404(contacts, id=contact_id)
    if request.method == 'POST':
        contact_instance.name = request.POST.get('name')
        contact_instance.email = request.POST.get('email')
        contact_instance.subject = request.POST.get('subject')
        contact_instance.message = request.POST.get('message')
        contact_instance.save()
        return redirect('del_app:show_contacts')
    return render(request, "edit_contact.html", {'contact': contact_instance})

def delete_contact(request, id):
    """ Deleting The contacts """
    contact_instance = get_object_or_404(contacts, id=id)
    contact_instance.delete()
    return redirect('del_app:show_contacts')

@login_required(login_url='accounts_app:login')
def booking_table(request):
    """ This is for the Table bookings page """
    if request.method == 'POST':
        bookings_instance = booking(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            people=request.POST['people'],
            message=request.POST['message'],
        )
        bookings_instance.save()
        return redirect('del_app:show_bookings')
    else:
        return render(request, 'book_table.html')

def show_bookings(request):
    """ Shows the bookings information """
    all_bookings = booking.objects.all()
    context = {'bookings': all_bookings}
    return render(request, 'show_bookings.html', context)

def update_booking(request, booking_id):
    """ Function to update an existing booking """
    bookings_instance = get_object_or_404(booking, id=booking_id)
    if request.method == 'POST':
        bookings_instance.name = request.POST.get('name')
        bookings_instance.email = request.POST.get('email')
        bookings_instance.phone = request.POST.get('phone')
        bookings_instance.date = request.POST.get('date')
        bookings_instance.time = request.POST.get('time')
        bookings_instance.people = request.POST.get('people')
        bookings_instance.message = request.POST.get('message')
        bookings_instance.save()
        return redirect('del_app:show_bookings')
    return render(request, "edit_booking.html", {'booking': bookings_instance})

def delete_booking(request, id):
    """ Deleting The bookings """
    bookings_instance = get_object_or_404(booking, id=id)
    bookings_instance.delete()
    return redirect('del_app:show_bookings')


# Adding the mpesa functionality
# Function to Display the payments form
def pay(request):
   """ Renders the form to pay """
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