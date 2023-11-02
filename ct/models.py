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
    #age = models.IntegerField(null=False, blank=False)
    #height = models.CharField(max_length=10, blank=True, null=True)  # Allow null values
    
     # height = models.IntegerField(blank=True, null=True)
    # height = models.CharField(max_length=10, blank=True)
    # weight = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username


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
    # booked_by = models.ManyToManyField(User, related_name='booked_doctors', blank=True)
    
    
    
    
    def __str__(self):
        return self.user.username



from django.conf import settings
from django.contrib.auth import get_user_model
class Booking(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slot_datetime = models.DateTimeField()
    # Add other booking-related fields





    