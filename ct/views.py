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
            
            return redirect("signin")
    else:
        return render(request, "drsignup.html")
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            if request.user.is_Customer:
                return redirect('/')
            elif request.user.is_Dietitian:
                return redirect('d_index')
            elif request.user.is_Doctor:
                return redirect('dr_index')
            elif request.user.is_superuser:
                return redirect('admindashboard')
        else:
            messages.success(request,("Invalid login credentials."))
    return render(request, 'signin.html')

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
    return redirect('index')  # Redirect to the home page after logout

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



