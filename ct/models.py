from django.db import models
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



   
    