from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes  
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.shortcuts import render

from django.core.mail import send_mail
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == 'POST':
        c_uname = request.POST.get('c_uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if (
            CustomUser.objects.filter(username=c_uname).exists()
        ):
            messages.error(request, "username already registered")
            return render(request, "signup.html")

        else:
            user = CustomUser.objects.create_user(
                username=c_uname,
                email=email,
                password=password,
                
                is_Customer=True,

            )
            user.save()
            # Generate a confirmation token for the user
            token = default_token_generator.make_token(user)

            # Encode the user's primary key for use in the URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))


            confirmation_link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
            confirmation_link = request.build_absolute_uri(confirmation_link)

            # Send the confirmation email to the user
            subject = 'Confirm your email'
            message = 'Please click the link below to confirm your email:\n\n' + confirmation_link
            from_email = 'irenehenry2024a@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
             # Display a success message
            messages.success(request, "Registration successful. You can now log in.")
            
            return redirect("signin")
    else:
        return render(request, "signup.html")


def dsignup(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if (
            CustomUser.objects.filter(username=username).exists()
        ):
            messages.error(request, "username already registered")
            return render(request, "dsignup.html")

        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                
                is_Dietitian=True,

            )
            user.save()
            # Generate a confirmation token for the user
            token = default_token_generator.make_token(user)

            # Encode the user's primary key for use in the URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))


            confirmation_link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
            confirmation_link = request.build_absolute_uri(confirmation_link)

            # Send the confirmation email to the user
            subject = 'Confirm your email'
            message = 'Please click the link below to confirm your email:\n\n' + confirmation_link
            from_email = 'irenehenry2024a@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
               # Display a success message
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("signin")
    else:
        return render(request, "dsignup.html")



def drsignup(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if (
            CustomUser.objects.filter(username=username).exists()
        ):
            messages.error(request, "username already registered")
            return render(request, "drsignup.html")

        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                
                is_Doctor=True,

            )
            user.save()
            # Generate a confirmation token for the user
            token = default_token_generator.make_token(user)

            # Encode the user's primary key for use in the URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))


            confirmation_link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
            confirmation_link = request.build_absolute_uri(confirmation_link)

            # Send the confirmation email to the user
            subject = 'Confirm your email'
            message = 'Please click the link below to confirm your email:\n\n' + confirmation_link
            from_email = 'irenehenry2024a@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            # Display a success message
            messages.success(request, "Registration successful. You can now log in.")
            
            return redirect("signin")
    else:
        return render(request, "drsignup.html")

# ...

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_Customer:  # Check if the user is a customer
                return redirect('/')  # Redirect to the index page
            elif user.is_Dietitian:
                return redirect('d_index')
            elif user.is_Doctor:
                return redirect('dr_index')
            elif user.is_superuser:
                return redirect('admindashboard')
        else:
            messages.error(request, "Invalid login credentials.")
    return render(request, 'signin.html')


# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request,user)
#             if request.user.is_Customer:
#                 return redirect('/')
#             elif request.user.is_Dietitian:
#                 return redirect('d_index')
#             elif request.user.is_Doctor:
#                 return redirect('dr_index')
#             elif request.user.is_superuser:
#                 return redirect('admindashboard')
#         else:
#             messages.success(request,("Invalid login credentials."))
#     return render(request, 'signin.html')

# @login_required(login_url='signin')
def admindashboard(request):
      
    # Fetch data for the admin dashboard here (e.g., user information, orders, statistics)
    # You can use Django's ORM to query the database for this data
    # Example:
    users = CustomUser.objects.all()
    #  username = Order.objects.all()
    
    context = {
        # Pass the fetched data to the template context
    'users': users ,
        
    }
    return render(request, "admindashboard.html",context)

def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
    except User.DoesNotExist:
        pass  # Handle the case when the user is not found

    return redirect('admindashboard')  # Redirect back to the admin dashboard or another appropriate URL


from django.contrib.auth import logout

def loggout(request):
    logout(request)
    return redirect('/')  # Redirect to the home page after logout

def d_index(request):
    return render(request, "d_index.html")


def dr_index(request):
    return render(request, "dr_index.html")

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        # Ensure that you have appropriate authorization checks here,
        # e.g., checking if the user is an admin and has permission to delete users.
        if request.user.is_authenticated and request.user.is_staff:
            user.delete()
    return redirect('admindashboard')
from django.contrib import admin
from .models import CustomUser



from django.shortcuts import redirect
from django.contrib.auth.models import User

def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active  # Toggle the user's status
        user.save()
    except User.DoesNotExist:
        pass  # Handle the case when the user is not found

    return redirect('admindashboard')  # Redirect back to the admin dashboard or another appropriate URL

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'confirmation_success.html')
        else:
            return render(request, 'confirmation_failure.html')
    except Exception as e:
        return render(request, 'confirmation_failure.html')

