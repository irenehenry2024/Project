from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    CUSTOMER = 1
    DIETITIAN = 2
    DOCTOR = 3

    ROLE_CHOICE = (
     (CUSTOMER, 'Customer'),
     (DIETITIAN, 'Dietitian'),
     (DOCTOR, 'Doctor'),
    )
    #username = None
    username = models.CharField(max_length=100,unique=True ,default='')
    #first_name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default=CUSTOMER)
    is_Customer = models.BooleanField(default=False)
    is_Dietitian = models.BooleanField(default=False)
    is_Doctor = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
        
    # def _str_(self):
    #     return self.username

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(null=True, blank=True)  # Allow null values
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Allow null value
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
     # Add a field to store BMI
    bmi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
   
    
    def __str__(self):
        return self.user.username
    #age = models.IntegerField(null=False, blank=False)
    #height = models.CharField(max_length=10, blank=True, null=True)  # Allow null values
    
    # height = models.IntegerField(blank=True, null=True)
    # height = models.CharField(max_length=10, blank=True)
    # weight = models.IntegerField(blank=True, null=True)


from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class DietitianProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    certifications = models.TextField()
    specialization = models.CharField(max_length=100)
    available_timings = models.CharField(max_length=255, blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username

from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    certifications = models.TextField()
    specialization = models.CharField(max_length=100)
    available_timings = models.CharField(max_length=255, blank=True, null=True)
    booked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='booked_doctors', blank=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)  # Add this line for the image field
    # booked_by = models.ManyToManyField(User, related_name='booked_doctors', blank=True)
    
    
    def __str__(self):
        return self.user.username


from django.contrib.auth.models import User

class DietitianProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    certifications = models.TextField()
    specialization = models.CharField(max_length=100)
    available_timings = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='dietitian_images/', blank=True, null=True)  # Add this line for the image field


    def __str__(self):
        return self.user.username



from django.db import models
from django.contrib.auth import get_user_model
from .models import DoctorProfile  # Import the DoctorProfile model
from datetime import date

class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # The user who made the booking
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)  # The doctor being booked
    booking_date = models.DateField(default=date(2023, 1, 1))  # Replace with your desired default date
    #booking_date =  models.DateField()  # Define a default value or use default=timezone.now if you want to set the current time

from django.db import models
from django.contrib.auth import get_user_model
from .models import DietitianProfile  # Import the DoctorProfile model
from datetime import date

class DietitianBooking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # The user who made the booking
    dietitian = models.ForeignKey(DietitianProfile, on_delete=models.CASCADE)  # The doctor being booked
    booking_date = models.DateField(default=date(2023, 1, 1))  # Replace with your desired default date



from django.db import models
from django.contrib.auth.models import User

# Model for food items
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    calories = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models

class FoodIntake(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    meal_time = models.CharField(max_length=10)  # 'breakfast', 'lunch', or 'dinner'
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ate {self.quantity} {self.food_item.name}'

    @property
    def consumed_calories(self):
        return self.quantity * self.food_item.calories

from django.db import models
from django.conf import settings

class ExerciseLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()  # Duration in minutes
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} on {self.date}"

from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professional_type = models.CharField(max_length=10)  # 'dietitian' or 'doctor'
    feedback_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    dietitian = models.ForeignKey(DietitianProfile, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Feedback'

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_message', 'dietitian', 'doctor']



# from django.conf import settings
# from django.contrib.auth import get_user_model
# class Booking(models.Model):
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     slot_datetime = models.DateTimeField()
#     # Add other booking-related fields





    