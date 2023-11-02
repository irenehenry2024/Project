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
# from django.contrib.auth import logout

# def logout_view(request):
#     logout(request)
#     return HttpResponse("Logged out successfully.")


from django.contrib.auth import logout

def loggout(request):
    logout(request)
    # return HttpResponse("Logged out successfully")
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

def customer_list(request):
    users = CustomUser.objects.filter(is_Customer=True)
    return render(request, 'customer_list.html', {'users': users})
    pass

def dietitian_list(request):
    users = CustomUser.objects.filter(is_Dietitian=True)
    return render(request, 'dietitian_list.html', {'users': users})
    pass

def doctor_list(request):
    users = CustomUser.objects.filter(is_Doctor=True)
    return render(request, 'doctor_list.html', {'users': users})
    pass

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



from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
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

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'user_profile.html', context)

from django.shortcuts import render, redirect
from .models import DietitianProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def duser_profile(request):
    try:
        duser_profile = DietitianProfile.objects.get(user=request.user)
    except DietitianProfile.DoesNotExist:
        # If the profile doesn't exist, create one for the user
        duser_profile = DietitianProfile(user=request.user)
        duser_profile.save()

    if request.method == 'POST':
        # Update the user profile with the data from the request
        duser_profile.phone_number = request.POST.get('num')
        duser_profile.state = request.POST.get('state')
        duser_profile.district = request.POST.get('district')
        duser_profile.gender = request.POST.get('gender')
        duser_profile.certifications = request.POST.get('certifications')
        duser_profile.specialization = request.POST.get('specialization')

        duser_profile.save()
        messages.success(request, 'Profile updated successfully.')

    context = {
        'duser_profile': duser_profile,
    }

    return render(request, 'duser_profile.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile

@login_required
def druser_profile(request):
    # Get or create the doctor profile for the current user
    try:
        druser_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        # If the profile doesn't exist, create one for the user
        druser_profile = DoctorProfile(user=request.user)
        druser_profile.save()

    if request.method == 'POST':
        if 'verify_doctor' in request.POST:
            # Handle the doctor verification process here
            druser_profile.is_verified = True
            druser_profile.save()
            messages.success(request, 'Doctor profile verified successfully.')
            # Redirect to a success page or back to the profile page
            return redirect('doctor_profile')  # Update to your URL name

        # Update the user profile with the data from the request
        druser_profile.phone_number = request.POST.get('phone_number')  # Make sure form field names match
        druser_profile.state = request.POST.get('state')
        druser_profile.district = request.POST.get('district')
        druser_profile.gender = request.POST.get('gender')
        druser_profile.certifications = request.POST.get('certifications')
        druser_profile.specialization = request.POST.get('specialization')
        druser_profile.available_timings = request.POST.get('available_timings')


        druser_profile.save()
        messages.success(request, 'Profile updated successfully.')

    context = {
        'druser_profile': druser_profile,
    }

    return render(request, 'druser_profile.html', context)

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

from .models import DoctorProfile
from django.shortcuts import render

def doctors_list(request):
    # Fetch a list of DoctorProfile objects
    doctors = DoctorProfile.objects.all()

    context = {
        'doctors': doctors,
    }

    return render(request, 'doctors_list.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import DoctorProfile
from django.contrib.admin.views.decorators import staff_member_required

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


# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ct.models import DoctorProfile

def book_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)

        # Perform the booking logic here (e.g., add the user to the doctor's booked_by field)
        # For demonstration purposes, we'll use a try-except block to handle exceptions.
        try:
            # Assuming the user is the currently logged-in user
            user = request.user
            doctor.booked_by.add(user)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def delete_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)

        # Perform the deletion logic here
        # For demonstration purposes, we'll use a try-except block to handle exceptions.
        try:
            doctor.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



