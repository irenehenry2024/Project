from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required

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
        else:
            messages.success(request,("Invalid login credentials."))
    return render(request, 'signin.html')

def index1(request):
    return render(request, 'index1.html')


from django.contrib.auth import logout

def loggout(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logout

def d_index(request):
    return render(request, "d_index.html")
def dr_index(request):
    return render(request, "dr_index.html")


# def signin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if email and password:
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 auth_login(request, user)

#                 if request.user.ROLE_CHOICE==CustomUser.CUSTOMER:
                
#                     return redirect('/')
#                 # elif request.user.user_typ == CustomUser.VENDOR:
#                 #     print("user is therapist")
#                 #     return redirect(reverse('therapist'))
#                 elif request.user.ROLE_CHOICE== CustomUser.DIETITIAN:
#                     print("user is Dietitian")                   
#                     return redirect('d_index')
#                 elif request.user.ROLE_CHOICE== CustomUser.DOCTOR:
#                     print("user is Doctor")                   
#                     return redirect('dr_index')


#                 # else:
#                 #     print("user is normal")
#                 #     return redirect('')

#             else:
#                 messages.success(request,("Invalid credentials."))
#         else:
#             messages.success(request,("Please fill out all fields."))
        
#     return render(request, 'signin.html')




    # if request.user.is_authenticated:
    #     if request.user.is_Customer:
    #         return redirect('index')
    #     elif request.user.is_Dietitian:
    #         return redirect('d_index')
    #     elif request.user.is_Doctor:
    #         return redirect('dr_index')

    
            #  else:
            # error_message = "Email and password are required fields."
            # return render(request, "signin.html", {"error_message": error_message})

    
        # if email and password:
           
            
                # if user.is_Customer:
                
                # elif user.is_Dietitian:
                #     return redirect('d_index')
                # elif user.is_Doctor:
                #     return redirect('dr_index')
            

       




# def signin(request):
#     if request.user.is_authenticated:
#         if request.user.is_Customer:
#             return redirect("index")
#         elif request.user.is_Dietitian:
#             return redirect("d_index")
#         elif request.user.is_Doctor:
#             return redirect("dr_index")
#         else:
#             return redirect("index")
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         if email and password:
#            user = authenticate(request, email=email, password=password)
            
#            if user is not None:
#             auth_login(request, user)
#             if user.is_Customer:
#                 return redirect("index")  # Redirect to customer index page
#             # Add an elif condition for seller if needed
#             elif user.is_Dietitian:
#                  return redirect("d_index")
#             elif user.is_Doctor:
#                  return redirect("dr_index")
#             else:
#                 return redirect("index")
#            else:
#                error_message = "Invalid login credentials."
#                return render(request, "signin.html", {"error_message": error_message})  # Use Django messages framework for error messages
                
#         else:
#             error_message = "Email and password are required fields."
#             return render(request, "signin.html", {"error_message": error_message})  # Use Django messages framework for error messages

#     return render(request, "signin.html")

# def signout(request):
#     pass


# def signup(request):
#     if request.method == 'POST':
#         userame = request.POST.get('uname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        

#         if (
#              CustomUser.objects.filter(email=email).exists()
#         ):
#             messages.error(request, "email already registered")
#             return render(request, "signin.html")

#         else:
#             user = CustomUser.objects.create_user(
#                 userame=username,
#                 email=email,
#                 password=password,
#                 is_Customer=True,

#             )
#             user.save()
#             return redirect("signin")
#     else:
#         return render(request, "signup.html")

# def dsignup(request):
#     if request.method == 'POST':
#         username = request.POST.get('uname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        

#         if (
#              CustomUser.objects.filter(email=email).exists()
#         ):
#             messages.error(request, "email already registered")
#             return render(request, "signin.html")

#         else:
#             user = CustomUser.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
                
#                 is_Dietitian=True,

#             )
#             user.save()
#             return redirect("signin")
#     else:
#         return render(request, "dsignup.html")

        
        # elif password != cpassword:
        #     messages.error(request, "Passwords do not match")
        # elif uname and email and password:
        #     user = CustomUser.objects.create_user(username=uname, email=email, password=password)
        #     user.is_Customer = True
        #     user.save()
        #     messages.success(request, "Registered as a customer successfully")
        #     return redirect('signin')
    
    
# def dsignup(request):
#     if request.method == 'POST':
#         uname = request.POST.get('uname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#         elif password != cpassword:
#             messages.error(request, "Passwords do not match")
#         elif uname and email and password:
#             user = CustomUser.objects.create_user(username=uname, email=email, password=password)
#             user.is_Dietitian = True
#             user.save()
#             messages.success(request, "Registered as a Dietitian successfully")
#             return redirect('signin')
    
#     return render(request, "dsignup.html")
# def drsignup(request):
#     if request.method == 'POST':
#         uname = request.POST.get('uname')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#         elif password != cpassword:
#             messages.error(request, "Passwords do not match")
#         elif uname and email and password:
#             user = CustomUser.objects.create_user(username=uname, email=email, password=password)
#             user.is_Doctor = True
#             user.save()
#             messages.success(request, "Registered as a Doctor successfully")
#             return redirect('signin')
    
#     return render(request, "dsignup.html")


       
