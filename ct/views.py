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

from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import login, authenticate
from .models import UserProfile 

from .models import Feedback
from .forms import FeedbackForm


# API Key: 02572699cea14f3c8aad5d8c26b32ae1

# Create your views here.



def index(request):
    return render(request, "index.html")

def recipe_catalog(request):
    return render(request, "recipe_catalog.html")

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LogMeals
import requests
import json

# Assume this function to get calories from API Ninja
def get_calories_from_api(name):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
    api_key = 'kqQ9bfS938jO+qjX74KnWg==HFoOm2P07PDOalEP'
    headers = {'X-Api-Key': api_key}

    try:
        api_request = requests.get(api_url + name, headers=headers)
        api_data = json.loads(api_request.content)

        # Check if the API response is successful
        if 'message' in api_data and api_data['message'] == 'success':
            return api_data['data'][0]['calories']
        else:
            return None  # Handle errors or invalid responses

    except Exception as e:
        print(e)
        return None  # Handle exceptions, return None for simplicity

@login_required
def log_meals(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        meal = request.POST.get('meal')

        # Fetch calorie information from API Ninja using the provided name
        calories = get_calories_from_api(name)

        if calories is not None:
            # Calculate total calories based on quantity
            total_calories = quantity * calories

            # Create a LogMeals object and save it to the database
            LogMeals.objects.create(
                user=request.user,
                name=name,
                quantity=quantity,
                calories=total_calories,
                meal=meal
            )
            return redirect('log_meals')  # Redirect to the same page after submitting the form

        else:
            # Handle the case when the API request fails or returns invalid data
            return render(request, 'log_meals.html', {'error_message': 'Failed to fetch calorie information'})

    context = {
        'log_meals': LogMeals.objects.filter(user=request.user),
    }
    return render(request, 'log_meals.html', context)


# from django.http import JsonResponse
# from django.shortcuts import render
# from .models import TimeSlot

# def add_slot(request):
#     if request.method == "POST":
#         session = request.POST.get('session')
#         time = request.POST.get('time')

#         if slot_exists(session, time):
#             return JsonResponse({'success': False, 'message': 'This time slot already exists.'})
#         else:
#             return handle_time_slot_creation(request, session, time)

#     slots = TimeSlot.objects.all()
#     return render(request, 'add_slot.html', {"slots": slots})

# def slot_exists(session, time):
#     return TimeSlot.objects.filter(session=session, time=time).exists()

# def handle_time_slot_creation(request, session, time):
#     if hasattr(request.user, 'dietitianprofile'):
#         dietitian = request.user.dietitian
#         slot = TimeSlot.objects.create(dietitian=dietitian, session=session, time=time)
#         return JsonResponse({'success': True, 'slot': {'session': slot.session, 'time': slot.time}})
#     else:
#         return JsonResponse({'success': False, 'message': 'User does not have a DietitianProfile.'})

from django.http import JsonResponse
from django.shortcuts import render
from .models import TimeSlot, DietitianProfile
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import CustomUser, TimeSlot

def add_slot(request):
    # Retrieve the CustomUser object or return a 404 response if it doesn't exist
    dietitian = get_object_or_404(CustomUser, username=request.user)

    if request.method == "POST":
        session = request.POST.get('session')
        time = request.POST.get('time')

        # Check if the time slot already exists for the given dietitian
        if TimeSlot.objects.filter(session=session, time=time, dietitian=dietitian).exists():
            return JsonResponse({'success': False, 'message': 'This time slot already exists.'})
        else:
            try:
                # Check if the user has a DietitianProfile
                dietitian_profile = dietitian.dietitianprofile
            except DietitianProfile.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User does not have a DietitianProfile.'})

            # Create the time slot
            slot = TimeSlot.objects.create(dietitian=dietitian, session=session, time=time)
            return JsonResponse({'success': True, 'slot': {'session': slot.session, 'time': slot.time}})

    # Fetch all existing slots for rendering on the page
    slots = TimeSlot.objects.all()
    return render(request, 'add_slot.html', {"slots": slots})



from django.http import JsonResponse
from django.shortcuts import render
from .models import DoctorSlot, DoctorProfile

def dr_addslot(request):

    doctor = get_object_or_404(CustomUser, username=request.user)

    if request.method == "POST":
        session = request.POST.get('session')
        time = request.POST.get('time')

        # Check if the time slot already exists
        if DoctorSlot.objects.filter(session=session, time=time, doctor=doctor).exists():
            return JsonResponse({'success': False, 'message': 'This time slot already exists.'})
        else:
            # Check if the user has a DoctorProfile
            if hasattr(request.user, 'doctorprofile'):
                doctor_profile = request.user.doctorprofile
                slot = DoctorSlot.objects.create(doctor=doctor, session=session, time=time)
                return JsonResponse({'success': True, 'slot': {'session': slot.session, 'time': slot.time}})
            else:
                return JsonResponse({'success': False, 'message': 'User does not have a DoctorProfile.'})

    slots = DoctorSlot.objects.all()
    return render(request, 'dr_addslot.html', {"slots": slots})

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.http import JsonResponse
# from .models import TimeSlot

# def add_slot(request):
#     if request.method == "POST":
#         session = request.POST.get('session')
#         time = request.POST.get('time')

#         # Check if the time slot already exists
#         if TimeSlot.objects.filter(session=session, time=time).exists():
#             return JsonResponse({'success': False, 'message': 'This time slot already exists.'})
#         else:
#             # Access the DietitianProfile associated with the user
#             dietitian_profile = request.user.dietitianprofile

#             # Check if the user is a dietitian and has a profile
#             if dietitian_profile:
#                 dietitian_id = dietitian_profile.id
#                 slot = TimeSlot.objects.create(dietitian_id=dietitian_id, session=session, time=time)
#                 return JsonResponse({'success': True, 'slot': {'session': slot.session, 'time': slot.time}})
#             else:
#                 return JsonResponse({'success': False, 'message': 'User is not a dietitian or does not have a profile.'})

#     slots = TimeSlot.objects.all()
#     return render(request, 'add_slot.html', {"slots": slots})


# def add_slot(request):
#     if request.method == "POST":
#         session = request.POST.get('session')
#         time = request.POST.get('time')
       
#         # Check if the time slot already exists
#         if TimeSlot.objects.filter(session=session, time=time).exists():
#             messages.error(request, 'This time slot already exists.')
#         else:
#             TimeSlot.objects.create(session=session, time=time)
#             messages.success(request, 'Slot added successfully.')  # Set success message
#             return redirect('duser_profile')  # Redirect to user_profile after successful slot addition

#     slots = TimeSlot.objects.all()
#     return render(request, 'add_slot.html', {"slots": slots})

# from .models import TimeSlot
# def add_slot(request):
#     if request.method == "POST":
#         session = request.POST.get('session')
#         time = request.POST.get('time')
       
#         # Check if the time slot already exists
#         if TimeSlot.objects.filter(session=session, time=time).exists():
#             messages.error(request, 'This time slot already exists.')
#         else:
#             TimeSlot.objects.create(session=session, time=time)
#             messages.success(request, 'Slot added successfully.')  # Set success message

#     slots = TimeSlot.objects.all()
#     return render(request, 'add_slot.html', {"slots": slots})




def calorie_counting(request):
    import requests
    import json

    if request.method == 'POST':
        query=request.POST['query']
        api_url='https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get (api_url + query, headers={'X-Api-Key': 'kqQ9bfS938jO+qjX74KnWg==HFoOm2P07PDOalEP'})

        try:
            api = json.loads(api_request.content)
            print(api_request.content)   
        except Exception as e:
            api = "oops there was an error"
            print(e)
        return render(request, 'calorie_counting.html',{'api':api})
    else:
        return render(request, 'calorie_counting.html',{'query':'Enter a valid query'})

# recipes/views.py
from django.shortcuts import render
import requests

def recipe_catalog(request):
    api_key = 'kqQ9bfS938jO+qjX74KnWg==HFoOm2P07PDOalEP'  # Replace with your Recipe Ninjas API key
    # app_id = 'YOUR_APP_ID'  # Replace with your Recipe Ninjas App ID

    # Make a request to the Recipe Ninjas API
    response = requests.get('https://api.api-ninjas.com/v1/recipe?query=', params={
        'format': 'json',
        'results': '10',  # You can adjust the number of results as needed
        'fields': 'item_name,nf_calories,nf_serving_size_qty,nf_serving_size_unit',
        # 'appId': app_id,
        'appKey': api_key,
    })

    # Check if the request was successful
    if response.status_code == 200:
        recipes = response.json().get('hits', [])
    else:
        recipes = []

    return render(request, 'recipe_catalog.html', {'recipes': recipes})

# import requests
# query = 'italian wedding soup'
# api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
# response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
# if response.status_code == requests.codes.ok:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)


    # query = '1lb brisket and fries'
    # api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    # response = requests.get(api_url, headers={'X-Api-Key': 'kqQ9bfS938jO+qjX74KnWg==HFoOm2P07PDOalEP'})
    # if response.status_code == requests.codes.ok:
    #    print(response.text)
    # else:
    #    print("Error:", response.status_code, response.text)
   


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

            # Create a UserProfile associated with the user
            user_profile = UserProfile(user=user)
            user_profile.save()

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
            user_profile = UserProfile(user=user)
            user_profile.save()


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
            user_profile = UserProfile(user=user)
            user_profile.save()

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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    return render(request, 'login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
def admindashboard(request):
    User = get_user_model()

    # Fetch data for the admin dashboard here
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = total_users - active_users
      
    # Fetch data for the admin dashboard here (e.g., user information, orders, statistics)
    # You can use Django's ORM to query the database for this data
    # Example:
    users = CustomUser.objects.all()
    customers= CustomUser.objects.filter(is_Customer=True)
    dietitians= CustomUser.objects.filter(is_Dietitian=True)
    doctors= CustomUser.objects.filter(is_Doctor=True)
    #  username = Order.objects.all()

    #  # Set a session variable to mark whether the user is authenticated
    # request.session['is_authenticated'] = True

    context = {
        # Pass the fetched data to the template context
    'users': users ,
    'total_users': total_users,
    'active_users': active_users,
    'inactive_users': inactive_users,
    'customers': User.objects.filter(is_Customer=True),
    'dietitians': User.objects.filter(is_Dietitian=True),
    'doctors': User.objects.filter(is_Doctor=True),
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
# from django.contrib.auth import logout

# def logout_view(request):
#     logout(request)
#     return HttpResponse("Logged out successfully.")


from django.contrib.auth import logout

def loggout(request):
    logout(request)
    # return HttpResponse("Logged out successfully")
    return redirect('/')  # Redirect to the home page after logout



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

def logout_view(request):
    # Clear the session variables
    request.session.flush()

    # Logout the user using Django's logout function
    logout(request)

    # Add a message for the user
    messages.info(request, 'You have been logged out.')

    # Redirect to the index page
    return redirect('/')


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




def ratings(request):
    return render(request, "ratings.html")


def dratings(request):
    return render(request, "dratings.html")



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import CustomUser  # Import your CustomUser model

def customer_list(request):
    users = CustomUser.objects.filter(is_Customer=True)

    # Set the number of users per page
    users_per_page = 10

    paginator = Paginator(users, users_per_page)
    page = request.GET.get('page',1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'customer_list.html', {'users': users})



# def customer_list(request):
#     users = CustomUser.objects.filter(is_Customer=True)
#     return render(request, 'customer_list.html', {'users': users})
#     pass
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import CustomUser  # Import your CustomUser model
def dietitian_list(request):
    users = CustomUser.objects.filter(is_Dietitian=True)
     # Set the number of users per page
    users_per_page = 10

    paginator = Paginator(users, users_per_page)
    page = request.GET.get('page',1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'dietitian_list.html', {'users': users})
    
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import CustomUser  # Import your CustomUser model
def doctor_list(request):
    users = CustomUser.objects.filter(is_Doctor=True)
     # Set the number of users per page
    users_per_page = 10

    paginator = Paginator(users, users_per_page)
    page = request.GET.get('page',1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'doctor_list.html', {'users': users})
    

from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If the profile doesn't exist, create one for the user
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        # Update the user profile with the data from the request
        user_profile.phone_number = request.POST.get('num')
        user_profile.state = request.POST.get('state')
        user_profile.district = request.POST.get('district')
        user_profile.gender = request.POST.get('gender')
        user_profile.age = request.POST.get('age')
        user_profile.height = request.POST.get('height')
        user_profile.weight = request.POST.get('weight')

        user_profile.save()
        messages.success(request, 'Profile updated successfully.')

        # Calculate BMI
        if user_profile.height and user_profile.weight:
           height_in_meters = float(user_profile.height) / 100  # Convert height to meters as a float
           weight_in_kg = float(user_profile.weight)  # Convert weight to kilograms as a float
           bmi = weight_in_kg / (height_in_meters ** 2)
           user_profile.bmi = bmi  # Save BMI in the user profile
           user_profile.save()


        # # Calculate BMI
        # if user_profile.height and user_profile.weight:
        #     height_in_meters = user_profile.height / 100  # Convert height to meters
        #     bmi = user_profile.weight / (height_in_meters ** 2)
        #     user_profile.bmi = bmi  # Save BMI in the user profile
        #     user_profile.save()

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'user_profile.html', context)



# from django.shortcuts import render, redirect
# from .models import UserProfile
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist

# @login_required
# def user_profile(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except ObjectDoesNotExist:
#         # If the profile doesn't exist, create one for the user
#         user_profile = UserProfile(user=request.user)
#         user_profile.save()

#     if request.method == 'POST':
#         # Update the user profile with the data from the request
#         user_profile.phone_number = request.POST.get('num')
#         user_profile.state = request.POST.get('state')
#         user_profile.district = request.POST.get('district')
#         user_profile.gender = request.POST.get('gender')
#         user_profile.age = request.POST.get('age')
#         user_profile.height = request.POST.get('height')
#         user_profile.weight = request.POST.get('weight')

#         user_profile.save()
#         messages.success(request, 'Profile updated successfully.')

#     # Calculate BMI
#     if user_profile.height and user_profile.weight:
#         height_in_meters = user_profile.height / 100  # Convert height to meters
#         bmi = user_profile.weight / (height_in_meters ** 2)
#         user_profile.bmi = bmi  # Save BMI in the user profile
#         user_profile.save() 

#     context = {
#         'user_profile': user_profile,
        
#     }

#     return render(request, 'user_profile.html', context)

from django.shortcuts import render, redirect
from .models import DietitianProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def duser_profile(request):
    try:
        dietitian = DietitianProfile.objects.get(user=request.user)
    except DietitianProfile.DoesNotExist:
        # If the profile doesn't exist, create one for the user
        dietitian = DietitianProfile(user=request.user)
        dietitian.save()
    if request.method == 'POST':
        if 'verify_dietitian' in request.POST:
            # Handle the dietitian verification process here
            dietitian.is_verified = True
            dietitian.save()
            messages.success(request, 'Dietitian profile verified successfully.')
            # Redirect to a success page or back to the profile page
            return redirect('dietitian_profile')  # Update to your URL name

        # Update the user profile with the data from the request
        dietitian.phone_number = request.POST.get('phone_number')
        dietitian.state = request.POST.get('state')
        dietitian.district = request.POST.get('district')
        dietitian.gender = request.POST.get('gender')
        dietitian.certifications = request.POST.get('certifications')
        dietitian.specialization = request.POST.get('specialization')
        dietitian.available_timings = request.POST.get('available_timings')

        if request.FILES.get('image'):
            dietitian.image = request.FILES['image']

        dietitian.save()
        messages.success(request, 'Profile updated successfully.')

         # Inside the section where you handle dietitian booking
        if 'book_dietitian' in request.POST:
        # Get the dietitian ID from the request
            dietitian_id = request.POST.get('dietitian_id')

        # Create a DietitianBooking instance
            booking = DietitianBooking.objects.create(user=request.user, dietitian_id=dietitian_id)

        if booking:
            messages.success(request, 'Booking successful.')
        else:
            messages.error(request, 'Booking failed. Please try again.')

    context = {
        'dietitian': dietitian,  
         # Pass the 'dietitian' object to the template
    }

    return render(request, 'duser_profile.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DietitianProfile, TimeSlot, DietitianBooking
from django.contrib import messages

@login_required

def dietitian_timeslots(request, dietitian_id):
    dietitian = get_object_or_404(CustomUser, id=dietitian_id, is_Dietitian=True)
    timeslots = TimeSlot.objects.filter(dietitian=dietitian)

    if request.method == 'POST':
        dietitian_id = request.POST.get('dietitian_id')
        session_date = request.POST.get('session_date')
        time_slot_id = request.POST.get('time_slot')

        try:
            # Retrieve the DietitianProfile instance
            dietitian = CustomUser.objects.get(id=dietitian_id, is_Dietitian=True)

            # Retrieve the TimeSlot instance
            time_slot = TimeSlot.objects.get(id=time_slot_id, dietitian=dietitian)

            # Calculate the amount (replace this with your own logic)
            amount = 500.00  # Replace with your own logic to calculate the amount

            # Create a new DietitianBooking instance
            booking = DietitianBooking.objects.create(
                user=request.user,
                dietitian=dietitian,
                booking_date=session_date,
                session=time_slot.session,
                time=time_slot.time,
                amount=amount
            )

            # Redirect to a success page or do something else
            messages.success(request, 'Booking successful!')
            return redirect('dietitian_payment',booking_id=booking.id)

        except CustomUser.DoesNotExist:
            messages.error(request, 'Dietitian not found.')
        except TimeSlot.DoesNotExist:
            messages.error(request, 'Time slot not found.')

    return render(request, 'book_dietitian.html', {'dietitian': dietitian, 'timeslots': timeslots})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, DoctorSlot, Booking
from django.contrib import messages

@login_required

def doctor_timeslots(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, is_Doctor=True)
    timeslots = DoctorSlot.objects.filter(doctor=doctor)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        session_date = request.POST.get('session_date')
        time_slot_id = request.POST.get('time_slot')

        try:
            # Retrieve the DietitianProfile instance
            doctor = CustomUser.objects.get(id=doctor_id, is_Doctor=True)

            # Retrieve the TimeSlot instance
            time_slot = DoctorSlot.objects.get(id=time_slot_id,doctor=doctor)

            # Calculate the amount (replace this with your own logic)
            amount = 500.00  # Replace with your own logic to calculate the amount

            # Create a new DietitianBooking instance
            booking = Booking.objects.create(
                user=request.user,
                doctor=doctor,
                booking_date=session_date,
                session=time_slot.session,
                time=time_slot.time,
                amount=amount
            )

            # Redirect to a success page or do something else
            messages.success(request, 'Booking successful!')
            return redirect('doctor_payment',booking_id=booking.id)

        except CustomUser.DoesNotExist:
            messages.error(request, 'Doctor not found.')
        except DoctorSlot.DoesNotExist:
            messages.error(request, 'Time slot not found.')

    return render(request, 'book_doctor.html', {'doctor': doctor, 'timeslots': timeslots})



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import DietitianBooking
# Authorize Razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def dietitian_payment(request, booking_id):
    try:
        dietitian_booking = DietitianBooking.objects.get(pk=booking_id)
    except DietitianBooking.DoesNotExist:
        # Handle case where booking is not found
        return HttpResponseBadRequest()

    currency = 'INR'
    amount = int(dietitian_booking.amount * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'http://127.0.0.1:8000/paymenthandler/{booking_id}/'

    # Pass these details to the frontend.
    context = {
        'dietitian_booking': dietitian_booking,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'dietitian_payment.html', context=context)


@csrf_exempt

def paymenthandler(request, booking_id):
    try:
        dietitian_booking = DietitianBooking.objects.get(pk=booking_id)
        dietitian_booking.is_paid = True
        dietitian_booking.save()

        # If you want to create a new DietitianBooking with is_paid=True, uncomment the following lines
        # booking = DietitianBooking.objects.create(is_paid=True)
        
        return redirect('dietitians_list')  # Assuming the correct URL name is 'dietitians_list'
    except DietitianBooking.DoesNotExist:
        # Handle case where booking is not found
        return HttpResponseBadRequest()


from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Booking
# Authorize Razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def doctor_payment(request, booking_id):
    try:
        dioctor_booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        # Handle case where booking is not found
        return HttpResponseBadRequest()

    currency = 'INR'
    amount = int(doctor_booking.amount * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'http://127.0.0.1:8000/payment/{booking_id}/'

    # Pass these details to the frontend.
    context = {
        'doctor_booking': doctor_booking,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'doctor_payment.html', context=context)


@csrf_exempt
def payment(request, booking_id):
    try:
        doctor_booking = Booking.objects.get(pk=booking_id)
        doctor_booking.is_paid = True
        doctor_booking.save()

        return redirect('doctors_list')  # Assuming the correct URL name is 'doctors_list'
    except Booking.DoesNotExist:
        # Handle case where booking is not found
        return HttpResponseBadRequest()


     






from django.shortcuts import render
from .models import DoctorSlot

def booking_doctor(request):
    # Assuming the user is logged in, you can access the current user
    current_user = request.user

    # Assuming TimeSlot model has a ForeignKey to User model
    # Adjust the model and field names accordingly
    timeslots = DoctorSlot.objects.filter(doctor=current_user.doctorprofile)

    # Pass the available time slots to the template
    return render(request, ' booking_doctor.html', {'timeslots': timeslots})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DietitianProfile, DietitianRating
from django.contrib import messages
from django.db.models import Avg

@login_required
def dietitian_ratings(request, dietitian_id):
    rating = request.POST.get('rating')
    review = request.POST.get('review')

    # Check if the user has already rated the dietitian
    existing_rating = DietitianRating.objects.filter(dietitian_id=dietitian_id, user=request.user).first()
    if existing_rating:
        messages.error(request, 'You have already rated this dietitian.')
    else:
        # Create a new rating
        DietitianRating.objects.create(dietitian_id=dietitian_id, user=request.user, rating=rating, review=review)
        messages.success(request, 'Rating submitted successfully.')

    # Redirect to the dietitian ratings page
    return redirect('dietitian_ratings_page', dietitian_id=dietitian_id)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DietitianProfile, DietitianRating
from django.db.models import Avg

@login_required
def dietitian_ratings_page(request, dietitian_id):
    # Fetch dietitian details
    dietitian = get_object_or_404(DietitianProfile, pk=dietitian_id)

    # Fetch all ratings for the dietitian
    ratings = DietitianRating.objects.filter(dietitian=dietitian)

    # Calculate average rating
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    context = {
        'dietitian': dietitian,
        'ratings': ratings,
        'average_rating': average_rating,
    }

    return render(request, 'ratings.html', context)






from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile

@login_required
def druser_profile(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        # If the profile doesn't exist, create one for the user
        doctor = DoctorProfile(user=request.user)
        doctor.save()

    if request.method == 'POST':
        if 'verify_doctor' in request.POST:
            # Handle the doctor verification process here
            doctor.is_verified = True
            doctor.save()
            messages.success(request, 'Doctor profile verified successfully.')
            # Redirect to a success page or back to the profile page
            return redirect('doctor_profile')  # Update to your URL name

        # Update the user profile with the data from the request
        doctor.phone_number = request.POST.get('phone_number')
        doctor.state = request.POST.get('state')
        doctor.district = request.POST.get('district')
        doctor.gender = request.POST.get('gender')
        doctor.certifications = request.POST.get('certifications')
        doctor.specialization = request.POST.get('specialization')
        doctor.available_timings = request.POST.get('available_timings')
        doctor.image = request.FILES.get("image")

        

        doctor.save()
        messages.success(request, 'Profile updated successfully.')

    context = {
        'doctor': doctor,  # Pass the 'doctor' object to the template
    }

    return render(request, 'druser_profile.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, DoctorRating
from django.contrib import messages
from django.db.models import Avg

@login_required
def doctor_ratings(request, doctor_id):
    rating = request.POST.get('rating')
    review = request.POST.get('review')

    # Check if the user has already rated the dietitian
    existing_rating = DoctorRating.objects.filter(doctor_id=doctor_id, user=request.user).first()
    if existing_rating:
        messages.error(request, 'You have already rated this dietitian.')
    else:
        # Create a new rating
        DoctorRating.objects.create(doctor_id=doctor_id, user=request.user, rating=rating, review=review)
        messages.success(request, 'Rating submitted successfully.')

    # Redirect to the dietitian ratings page
    return redirect('doctor_ratings_page', doctor_id=doctor_id)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, DoctorRating
from django.db.models import Avg

@login_required
def doctor_ratings_page(request, doctor_id):
    # Fetch dietitian details
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)

    # Fetch all ratings for the dietitian
    ratings = DoctorRating.objects.filter(doctor=doctor)

    # Calculate average rating
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    context = {
        'doctor': doctor,
        'ratings': ratings,
        'average_rating': average_rating,
    }

    return render(request, 'dratings.html', context)

from django.db.models import Q
from django.shortcuts import render, redirect
from .models import DoctorProfile, Booking, DoctorRating

def doctors_list(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        doctor_id = request.POST.get('doctor_id')

        # Check if doctor_id and user_id are not None and are valid
        if doctor_id is not None and user_id is not None:
            try:
                doctor_id = int(doctor_id)  # Convert to an integer if it's a string
                user_id = int(user_id)  # Convert to an integer if it's a string
            except (TypeError, ValueError):
                # Handle invalid values
                return redirect('doctors_list')  # Redirect to the same page or show an error message

            # Create a Booking instance
            booking = Booking.objects.create(user_id=user_id, doctor_id=doctor_id)

            if booking:
                return redirect('doctors_list')  # Redirect to the page after successful booking
            else:
                # Handle booking failure
                return redirect('doctors_list')  # Redirect to the same page or show an error message

    # Fetch a list of DoctorProfile objects
    doctors = DoctorProfile.objects.all()

    for doctor in doctors:
        doctor.avg_rating = doctor.average_rating()
        doctor.total_ratings = doctor.total_ratings()

    # Handling GET (search) request
    search_query = request.GET.get('search', '')

    # Filter doctors based on the search query
    if search_query:
        doctors = doctors.filter(
            Q(user__username__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )

    context = {
        'doctors': doctors,
    }

    return render(request, 'doctors_list.html', context)


from django.db.models import Q
from django.shortcuts import render, redirect
from .models import DietitianProfile, DietitianBooking, DietitianRating

def dietitians_list(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        dietitian_id = request.POST.get('dietitian_id')

        # Check if dietitian_id and user_id are not None and are valid
        if dietitian_id is not None and user_id is not None:
            try:
                dietitian_id = int(dietitian_id)  # Convert to an integer if it's a string
                user_id = int(user_id)  # Convert to an integer if it's a string
            except (TypeError, ValueError):
                # Handle invalid values
                return redirect('dietitians_list')  # Redirect to the same page or show an error message

            # Create a Booking instance
            booking = DietitianBooking.objects.create(user_id=user_id, dietitian_id=dietitian_id)

            if booking:
                return redirect('dietitians_list')  # Redirect to the page after successful booking
            else:
                return redirect('dietitians_list')  # Handle booking failure
        else:
            # Handle missing dietitian_id or user_id
            return redirect('dietitians_list')  # Redirect to the same page or show an error message
    else:  # Handling GET (search) request
        search_query = request.GET.get('search', '')


    # Fetch a list of DietitianProfile objects
    dietitians = DietitianProfile.objects.all()

    for dietitian in dietitians:
        dietitian.avg_rating = dietitian.average_rating()
        dietitian.total_ratings = dietitian.total_ratings()


    # Filter dietitians based on the search query
    if search_query:
        dietitians = dietitians.filter(
            Q(user__username__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(specialization__icontains=search_query)
            )  

    context = {
        'dietitians': dietitians,
    }

    return render(request, 'dietitians_list.html', context)



   
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Booking

@staff_member_required
def doctor_profile(request):
    # Get a list of doctor profiles
    doctors = DoctorProfile.objects.all()
    
    context = {
        'doctors': doctors,
        
    }
    return render(request, 'doctor_profile.html', context)

from django.contrib import messages
@staff_member_required
def verify_doctor(request, doctor_id):
    # Get the doctor profile
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    
    # Verify the doctor
    doctor.verified = True
    doctor.save()

      # Send a success message to the doctor
    messages.success(request, f'Doctor {doctor.user.username} has been successfully verified.')
    
    # Redirect back to the list of doctor profiles
    return redirect('doctor_profile')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import DoctorProfile

@staff_member_required
def decline_doctor(request, doctor_id):
    # Get the doctor profile
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    
    # Decline the doctor
    doctor.declined = True
    doctor.save()

    # Send a message to the doctor
    messages.error(request, f'Doctor {doctor.user.username} has been declined.')

    # Redirect back to the list of doctor profiles
    return redirect('doctor_profile')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dietitian_profile(request):
    # Get a list of dietitian profiles
    dietitians = DietitianProfile.objects.all()
   
    
    context = {
        'dietitians': dietitians,
       
    }
    return render(request, 'dietitian_profile.html', context)

from django.contrib import messages
@staff_member_required
def verify_dietitian(request, dietitian_id):
    # Get the dietitian profile
    dietitian = get_object_or_404(DietitianProfile, pk=dietitian_id)
    
    # Verify the doctor
    dietitian.verified = True
    dietitian.save()

      # Send a success message to the dietitian
    messages.success(request, f'Dietitian {dietitian.user.username} has been successfully verified.')
    
    # Redirect back to the list of doctor profiles
    return redirect('dietitian_profile')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import DietitianProfile

@staff_member_required
def decline_dietitian(request, dietitian_id):
    # Get the doctor profile
    dietitian = get_object_or_404(DietitianrProfile, pk=dietitian_id)
    
    # Decline the doctor
    dietitian.declined = True
    dietitian.save()

    # Send a message to the doctor
    messages.error(request, f'Doctor {dietitian.user.username} has been declined.')

    # Redirect back to the list of doctor profiles
    return redirect('dietitian_profile')


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')  # Get the old password from the form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user  # Get the currently logged-in user

        # Check if the entered old password matches the user's current password
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            # Change the user's password and save it to the database
            user.set_password(new_password)
            user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')
    
from django.http import JsonResponse
from .models import DoctorProfile
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def book_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        print(f'doctor_id received: {doctor_id}')

        try:
            doctor = get_object_or_404(DoctorProfile, id=doctor_id)
            user = request.user

            if Booking.objects.filter(doctor=doctor, user=user).exists():
                return JsonResponse({'success': False, 'message': 'You have already booked this doctor.'})

            booking = Booking(doctor=doctor, user=user)
            booking.save()

            return JsonResponse({'success': True, 'message': 'Booking successful.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})


def view_doctor_details(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)

            # You can do some additional processing here if needed

            return JsonResponse({'success': True, 'message': 'Doctor details retrieved successfully.'})
        except DoctorProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Doctor not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})

from django.http import JsonResponse
from .models import DietitianProfile
from .models import DietitianBooking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def book_dietitian(request):
    if request.method == 'POST':
        dietitian_id = request.POST.get('dietitian_id')
        print(f'dietitian_id received: {dietitian_id}')

        try:
           dietitian = get_object_or_404(DietitianProfile, id=dietitian_id)
           user = request.user

           if DietitianBooking.objects.filter(dietitian=dietitian, user=user).exists():
               return JsonResponse({'success': False, 'message': 'You have already booked this dietitian.'})

           booking = DietitianBooking(dietitian=dietitian, user=user)
           booking.save()

           return JsonResponse({'success': True, 'message': 'Booking successful.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})


def view_dietitian_details(request):
    if request.method == 'POST':
        dietitian_id = request.POST.get('dietitian_id')

        try:
            dietitian = DietitianProfile.objects.get(id=dietitian_id)

            # You can do some additional processing here if needed

            return JsonResponse({'success': True, 'message': 'Dietitian details retrieved successfully.'})
        except DietitianProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Dietitian not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})


# from django.http import JsonResponse
# from .models import DietitianProfile
# from .models import DietitianBooking  # Import the Booking model if you have one

# def book_dietitian(request):
#     if request.method == 'POST':
#         dietitian_id = request.POST.get('dietitian_id')

#         try:
#             dietitian = DietitianProfile.objects.get(id=dietitian_id)
#             user = request.user

#             # Check if the user has already booked this dietitian
#             if dietitian.booked_by.filter(id=user.id).exists():
#                 return JsonResponse({'success': False, 'message': 'You have already booked this doctor.'})

#             # Create a Booking instance and link it to the selected dietitian and the logged-in user
#             booking = DietitianBooking(dietitian=dietitian, user=user)
#             booking.save()

#             return JsonResponse({'success': True, 'message': 'Booking successful.'})
#         except DietitianProfile.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Dietitian not found.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})




from django.shortcuts import render, redirect
from .models import UserProfile, FoodItem, FoodIntake
from django.db.models import Sum
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .models import UserProfile, FoodItem, FoodIntake


def food_intake(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        age = int(request.POST.get('age'))
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))

        # You can create or update the user's profile based on username
        user, created = UserProfile.objects.get_or_create(
            username=username,
            defaults={'gender': gender, 'age': age, 'height': height, 'weight': weight}
        )

        food_item_id = request.POST.get('food_item')
        meal_time = request.POST.get('meal_time')
        quantity = float(request.POST.get('quantity'))
        food_item = FoodItem.objects.get(pk=food_item_id)

        # Create a FoodIntake record for the user
        FoodIntake.objects.create(user=user, food_item=food_item, meal_time=meal_time, quantity=quantity)

        return redirect('food_intake_list')

    users = UserProfile.objects.all()
    food_items = FoodItem.objects.all()
    return render(request, 'food_intake.html', {'users': users, 'food_items': food_items})

def food_intake_list(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = UserProfile.objects.get(pk=user_id)
        food_intake = FoodIntake.objects.filter(user=user)
        total_calories = food_intake.aggregate(Sum('consumed_calories'))['consumed_calories__sum']
        return HttpResponse(f"Total consumed calories for {user.username}: {total_calories} calories")

    users = UserProfile.objects.all()
    return render(request, 'food_intake_list.html', {'users': users})

from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def bmi_estimation(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.height and user_profile.weight:
        height_in_meters = user_profile.height / 100  # Convert height to meters
        bmi = user_profile.weight / (height_in_meters ** 2)
        user_profile.bmi = bmi  # Save BMI in the user profile
        user_profile.save()
     # Calculate BMR (Basal Metabolic Rate)
        if user_profile.gender == 'M':
            bmr = 88.362 + (13.397 * user_profile.weight) + (4.799 * user_profile.height) - (5.677 * user_profile.age)
        elif user_profile.gender == 'F':
            bmr = 447.593 + (9.247 * user_profile.weight) + (3.098 * user_profile.height) - (4.330 * user_profile.age)
        else:
            bmr = 0

        if request.method == 'POST':
        # Assuming 'activity_level' is in the POST data
           activity_level = request.POST.get('activity_level')
           user_profile.activity_level = activity_level

        # Calculate total calorie intake based on activity level
        activity_level_multiplier = {
            'Sedentary': 1.2,
            'Lightly Active': 1.375,
            'Moderately Active': 1.55,
            'Active': 1.725,
            'Very Active': 1.9,
        }

        activity_level = user_profile.activity_level
        total_calorie_intake = bmr * activity_level_multiplier.get(activity_level, 1.2)

    context = {
        'user_profile': user_profile,
        'total_calorie_intake': total_calorie_intake,
    }

    return render(request, 'bmi_estimation.html', context)

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404  # Import get_object_or_404
from .models import DoctorProfile, Booking

def dr_bookings(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id)  # Use get_object_or_404 for graceful handling
    
    bookings = Booking.objects.filter(doctor_id=doctor_id)
    users_who_booked = [booking.user for booking in bookings]
    


    context = {
        'doctor': doctor,
        'users_who_booked': users_who_booked,
    }

    return render(request, 'dr_bookings.html', context)


from .models import DietitianProfile, DietitianBooking

def d_bookings(request, dietitian_id):
    # Use get_object_or_404 to retrieve the DietitianProfile or return a 404 response if it doesn't exist
    dietitian = get_object_or_404(CustomUser, id=dietitian_id)
    
    # Retrieve all bookings for the specified dietitian
    bookings = DietitianBooking.objects.filter(dietitian_id=dietitian_id)

    users_who_booked = [booking.user for booking in bookings]

    context = {
        'dietitian':  dietitian,
        'bookings': bookings,
        'users_who_booked': users_who_booked,
    }

    return render(request, 'd_bookings.html', context)



from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib import messages

def log_exercise(request):
    if request.method == 'POST':
        # Handle form submission here
        exercise_name = request.POST.get('exercise_name')
        duration = request.POST.get('duration')
        date = request.POST.get('date')

        # Perform any necessary processing or database operations here
        # For example, you can save the exercise log to your database

        messages.success(request, 'Exercise logged successfully.')
        return redirect('log_exercise')  # Redirect to the same page after successful submission

    return render(request, 'log_exercise.html')

# views.py
from django.shortcuts import render, redirect
from .models import Feedback, DoctorProfile, DietitianProfile

def submit_feedback(request):
    if request.method == 'POST':
        professional_type = request.POST.get('professional_type')
        feedback_message = request.POST.get('feedback_message')

        # Get the current user and their profile
        user = request.user
        user_profile = None

        # Determine the professional type and set the appropriate profile
        if professional_type == 'Doctor':
            user_profile = user.doctorprofile
        elif professional_type == 'Dietitian':
            user_profile = user.dietitianprofile

        # Create the feedback object
        feedback = Feedback.objects.create(
            professional_type=professional_type,
            feedback_message=feedback_message,
            user=user,
        )

        # Set the appropriate doctor or dietitian based on professional_type
        if professional_type == 'Doctor':
            feedback.doctor = user_profile
        elif professional_type == 'Dietitian':
            feedback.dietitian = user_profile

        feedback.save()

        return redirect('submit_feedback.html')  # Redirect to a success page

    return render(request, 'submit_feedback.html', {})

# views.py

from django.shortcuts import render
from .models import Feedback, DoctorProfile, DietitianProfile

def dr_feedback(request):
    # Assuming you have a DoctorProfile linked to the current user
    doctor_profile = request.user.doctorprofile

    # Get feedback specific to the doctor
    professional_feedback = Feedback.objects.filter(doctor=doctor_profile)

    return render(request, 'dr_feedback.html', {'professional_feedback': professional_feedback})

def d_feedback(request):
    # Assuming you have a DietitianProfile linked to the current user
    dietitian_profile = request.user.dietitianprofile

    # Get feedback specific to the dietitian
    professional_feedback = Feedback.objects.filter(dietitian=dietitian_profile)

    return render(request, 'd_feedback.html', {'professional_feedback': professional_feedback})


# from django.shortcuts import render, redirect
# from .models import Feedback, DoctorProfile, DietitianProfile

# def submit_feedback(request):
#     if request.method == 'POST':
#         professional_type = request.POST.get('professional_type')
#         feedback_message = request.POST.get('feedback_message')

#         # Get the current user and their profile
#         user = request.user
#         user_profile = None

#         if professional_type == 'Doctor':
#             user_profile = user.DoctorProfile
#         elif professional_type == 'Dietitian':
#             user_profile = user.DietitianProfile


#         # Create the feedback object
#         feedback = Feedback.objects.create(
#             professional_type=professional_type,
#             feedback_message=feedback_message,
#             user=user,
#             doctor=user_profile if professional_type == 'Doctor' else None,
#             dietitian=user_profile if professional_type == 'Dietitian' else None,
#         )

#         return redirect('submit_feedback.html')  # Redirect to a success page

#     return render(request, 'submit_feedback.html', {})

# from .models import DietitianProfile, DoctorProfile, Feedback
# from .forms import FeedbackForm

# def submit_feedback(request, professional_type, professional_id):
#     if professional_type == 'dietitian':
#         professional = DietitianProfile.objects.get(id=professional_id)
#         feedback_template = 'd_feedback.html'  # Template for dietitians
#     elif professional_type == 'doctor':
#         professional = DoctorProfile.objects.get(id=professional_id)
#         feedback_template = 'dr_feedback.html'  # Template for doctors

#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.professional = professional
#             feedback.save()
#             messages.success(request, 'Feedback submitted successfully.')
#             return render(request, feedback_template, {'professional': professional, 'feedback': feedback})
#             # Redirecting to the feedback page with the feedback message

#     else:
#         form = FeedbackForm()

#     return render(request, 'submit_feedback.html', {'form': form, 'professional': professional, 'professional_type': professional_type, 'professional_id': professional_id})

# def d_feedback(request, professional_id):
#     dietitian = DietitianProfile.objects.get(id=professional_id)
#     feedback_messages = Feedback.objects.filter(professional=dietitian)

#     return render(request, 'd_feedback.html', {'dietitian': dietitian, 'feedback_messages': feedback_messages})

# def dr_feedback(request, professional_id):
#     doctor = DoctorProfile.objects.get(id=professional_id)
#     feedback_messages = Feedback.objects.filter(professional=doctor)

#     return render(request, 'dr_feedback.html', {'doctor': doctor, 'feedback_messages': feedback_messages})

# from .models import DietitianProfile, DoctorProfile, Feedback
# from .forms import FeedbackForm

# def submit_feedback(request, professional_type, professional_id):
#     if professional_type == 'dietitian':
#         professional = DietitianProfile.objects.get(id=professional_id)

#     elif professional_type == 'doctor':
#         professional = DoctorProfile.objects.get(id=professional_id)

#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)

#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.professional = professional
#             feedback.save()
#             messages.success(request, 'Feedback submitted successfully.')
#             return redirect('professional_profile', professional_type, professional_id)

#     else:
#         form = FeedbackForm()

#     return render(request, 'submit_feedback.html', {'form': form, 'professional': professional, 'professional_type': professional_type, 'professional_id': professional_id})
# views.py

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback

@login_required
def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user to the feedback
            feedback.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect('user_profile')  # Redirect to a success page after submission

    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})






# from django.shortcuts import render, redirect
# from .models import DietitianProfile, DietitianBooking

# def dietitians_list(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         dietitian_id = request.POST.get('dietitian_id')

#          # Check if the dietitian_id is not None and user_id is valid (add appropriate validation)
#         if dietitian_id is not None and user_id is not None:
#             # Create a Booking instance
#             booking = DietitianBooking.objects.create(user_id=user_id, dietitian_id=dietitian_id)

#             if booking:
#                 return redirect('dietitians_list')
#             else:
#                 return redirect('dietitians_list')

#     # Fetch a list of DoctorProfile objects
#     dietitians = DietitianProfile.objects.all()

#     context = {
#         'dietitians': dietitians,
#     }

#     return render(request, 'dietitians_list.html', context)



# # views.py
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from ct.models import DoctorProfile

# def book_doctor(request):
#     if request.method == 'POST':
#         doctor_id = request.POST.get('doctor_id')
#         doctor = get_object_or_404(DoctorProfile, id=doctor_id)

#         # Perform the booking logic here (e.g., add the user to the doctor's booked_by field)
#         # For demonstration purposes, we'll use a try-except block to handle exceptions.
#         try:
#             # Assuming the user is the currently logged-in user
#             user = request.user
#             doctor.booked_by.add(user)
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# def delete_doctor(request):
#     if request.method == 'POST':
#         doctor_id = request.POST.get('doctor_id')
#         doctor = get_object_or_404(DoctorProfile, id=doctor_id)

#         # Perform the deletion logic here
#         # For demonstration purposes, we'll use a try-except block to handle exceptions.
#         try:
#             doctor.delete()
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm

# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Update the session to prevent the user from being logged out
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')  # Redirect to the same page after successful password change
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(user=request.user)
#     return render(request, 'change_password.html', {
#         'form': form
#     })


# views.py
# from django.shortcuts import render, get_object_or_404
# from .models import DoctorProfile, Booking

# def booked_doctors_list(request):
#     # Fetch a list of booked doctors
#     booked_doctors = DoctorProfile.objects.filter(booking__isnull=False)

#     context = {
#         'booked_doctors': booked_doctors,
#     }

#     return render(request, 'booked_doctors_list.html', context)

# def booked_doctor_details(request, doctor_id):
#     doctor = get_object_or_404(DoctorProfile, id=doctor_id)
#     bookings = Booking.objects.filter(doctor=doctor)

#     context = {
#         'doctor': doctor,
#         'bookings': bookings,
#     }

#     return render(request, 'booked_doctor_details.html', context)


# from django.shortcuts import render, redirect
# from .models import DoctorProfile
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required
# def druser_profile(request):
#     try:
#         druser_profile = DoctorProfile.objects.get(user=request.user)
#     except DoctorProfile.DoesNotExist:
#         # If the profile doesn't exist, create one for the user
#         druser_profile = DoctorProfile(user=request.user)
#         druser_profile.save()

#     if request.method == 'POST':
#         if 'verify_doctor' in request.POST:
#             # Handle the doctor verification process here
#             druser_profile.is_verified = True
#             druser_profile.save()
#             messages.success(request, 'Doctor profile verified successfully.')
#             return redirect('some_success_url')  # Redirect to a success page

#         # Update the user profile with the data from the request
#         druser_profile.phone_number = request.POST.get('num')
#         druser_profile.state = request.POST.get('state')
#         druser_profile.district = request.POST.get('district')
#         druser_profile.gender = request.POST.get('gender')
#         druser_profile.certifications = request.POST.get('certifications')
#         druser_profile.specialization = request.POST.get('specialization')

#         druser_profile.save()
#         messages.success(request, 'Profile updated successfully.')

#     context = {
#         'druser_profile': druser_profile,
#     }

#     return render(request, 'druser_profile.html', context)

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
# from .models import DoctorProfile  # Import your UserProfile model

# @login_required
# def druser_profile(request):
#     druser_profile = DoctorProfile.objects.get(user=request.user)
#     try:
#        druser_profile = DoctorProfile.objects.get(user=request.user)

#     except ObjectDoesNotExist:
#         # If the profile doesn't exist, create one for the user
#         druser_profile = DoctorProfile(user=request.user)
#         druser_profile.save()

#     if request.method == 'POST':
#         # Update the user profile with the data from the request
#         druser_profile.phone_number = request.POST.get('num')
#         druser_profile.state = request.POST.get('state')
#         druser_profile.district = request.POST.get('district')
#         druser_profile.gender = request.POST.get('gender')
#         druser_profile.certifications = request.POST.get('certifications')
#         druser_profile.specialization = request.POST.get('specialization')
        

#         druser_profile.save()
#         messages.success(request, 'Profile updated successfully.')

#     context = {
#         'druser_profile': druser_profile,
#     }

#     return render(request, 'druser_profile.html', context)


# from django.shortcuts import render
# from .models import DoctorProfile

# def doctors_list(request):
#     doctors = DoctorProfile.objects.all()
#     return render(request, 'doctors_list.html', {'doctors': doctors})


# from django.shortcuts import render, redirect
# from .models import DoctorProfile
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required
# def druser_profile(request):
#     try:
#         druser_profile = DoctorProfile.objects.get(user=request.user)
#     except DoctorProfile.DoesNotExist:
#         # If the profile doesn't exist, create one for the user
#         druser_profile = DoctorProfile(user=request.user)
#         druser_profile.save()

#     if request.method == 'POST':
#         # Update the user profile with the data from the request
#         druser_profile.phone_number = request.POST.get('num')
#         druser_profile.state = request.POST.get('state')
#         druser_profile.district = request.POST.get('district')
#         druser_profile.gender = request.POST.get('gender')
#         druser_profile.certifications = request.POST.get('certifications')
#         druser_profile.specialization = request.POST.get('specialization')

#         druser_profile.save()
#         messages.success(request, 'Profile updated successfully.')

#     context = {
#         'druser_profile': druser_profile,
#     }

#     return render(request, 'druser_profile.html', context)

# from django.shortcuts import render, redirect
# from .models import DietitianProfile
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
# @login_required
# def duser_profile(request):
#     duser_profile = DietitianProfile.objects.get(user=request.user)
#     try:
#         duser_profile = DietitianProfile.objects.get(user=request.user)
#     except ObjectDoesNotExist:
#         # If the profile doesn't exist, create one for the user
#         duser_profile = DietitianProfile(user=request.user)
#         duser_profile.save()

#     if request.method == 'POST':
#         # Update the user profile with the data from the request
#         duser_profile.phone_number = request.POST.get('num')
#         duser_profile.state = request.POST.get('state')
#         duser_profile.district = request.POST.get('district')
#         duser_profile.gender = request.POST.get('gender')
#         duser_profile.certifications = request.POST.get('certifications')
#         duser_profile.specialization = request.POST.get('specialization')
        

#         duser_profile.save()
#         messages.success(request, 'Profile updated successfully.')

#     context = {
#         'duser_profile': duser_profile,
#     }

#     return render(request, 'duser_profile.html', context)

# from django.http import JsonResponse
# from django.contrib.auth.models import User

# def update_user_status(request, user_id, new_status):
#     try:
#         user = User.objects.get(id=user_id)
#         user.is_active = new_status == "active"
#         user.save()
#         return JsonResponse({"newStatus": "active" if user.is_active else "inactive"})
#     except User.DoesNotExist:
#         return JsonResponse({"error": "User not found"}, status=404)



# def set_session(request):
#     # Set a value in the session
#     request.session['user_id'] = 1
#     return HttpResponse("Session data set successfully.")

# def get_session(request):
#     # Get a value from the session
#     user_id = request.session.get('user_id', None)
#     if user_id is not None:
#         return HttpResponse(f"User ID from session: {user_id}")
#     else:
#         return HttpResponse("User ID not found in session.")


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
    

