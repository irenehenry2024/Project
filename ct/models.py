from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.urls import reverse

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
    # bmr = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # Add BMR field
    activity_level = models.CharField(max_length=20, blank=True, null=True)
    # activity_level = models.CharField(max_length=20, choices=[
    #     ('Sedentary', 'Sedentary'),
    #     ('Lightly Active', 'Lightly Active'),
    #     ('Moderately Active', 'Moderately Active'),
    #     ('Active', 'Active'),
    #     ('Very Active', 'Very Active'),
    # ], blank=True, null=True)  # Add activity level field
    
   
    
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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

    def average_rating(self):
        # Calculate the average rating using the related DietitianRating instances
        ratings = DoctorRating.objects.filter(doctor=self)
        if ratings.exists():
            average = ratings.aggregate(Avg('rating'))['rating__avg']
            return round(average, 1)
        return 0.0

    def total_ratings(self):
        # Get the total number of ratings for the dietitian
        return DoctorRating.objects.filter(doctor=self).count()




from django.db import models
from django.conf import settings
from django.db.models import Avg
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

    def average_rating(self):
        # Calculate the average rating using the related DietitianRating instances
        ratings = DietitianRating.objects.filter(dietitian=self)
        if ratings.exists():
            average = ratings.aggregate(Avg('rating'))['rating__avg']
            return round(average, 1)
        return 0.0

    def total_ratings(self):
        # Get the total number of ratings for the dietitian
        return DietitianRating.objects.filter(dietitian=self).count()



from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name ='dr_bookings')  # The user who made the booking
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name ='doctor_bookings')  # The doctor being booked
    booking_date = models.DateField()  # Replace with your desired default date
    session = models.CharField(max_length=255, default='afternoon')
    time = models.CharField(max_length=5, default='09:00')
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)  # New field for payment status

    @property
    def doctor_id(self):
        return self.doctor.user.id if self.doctor and self.doctor.user else None

    def __str__(self):
        return f"{self.user} booked with {self.doctor} on {self.booking_date} for {self.session} at {self.time} with amount {self.amount}. Paid: {self.is_paid}"





# from django.db import models
# from django.contrib.auth import get_user_model
# from .models import DietitianProfile  # Import the DoctorProfile model
# from datetime import date

# class DietitianBooking(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_bookings')
#     dietitian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dietitian_bookings')
#     booking_date = models.DateField(default=date(2023, 1, 1))  # Replace with your desired default date
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class DietitianBooking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_bookings')
    dietitian = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='dietitian_bookings')
    booking_date = models.DateField()  # No default date, the user will provide the date
    session = models.CharField(max_length=255, default='afternoon')
    time = models.CharField(max_length=5, default='09:00')
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)  # New field for payment status


    # Add any additional fields you need for the DietitianBooking model
    @property
    def dietitian_id(self):
        return self.dietitian.user.id if self.dietitian and self.dietitian.user else None

    def __str__(self):
        return f"{self.user} booked with {self.dietitian} on {self.booking_date} for {self.session} at {self.time} with amount {self.amount}. Paid: {self.is_paid}"



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

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Feedback(models.Model):
    professional_type_choices = [
        ('Doctor', 'Doctor'),
        ('Dietitian', 'Dietitian'),
    ]

    professional_type = models.CharField(max_length=20, choices=professional_type_choices)
    feedback_message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Reference to the respective professional model
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, null=True, blank=True)
    dietitian = models.ForeignKey(DietitianProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

    class Meta:
        ordering = ['-timestamp']



# class Feedback(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     professional_type = models.CharField(max_length=10)  # 'dietitian' or 'doctor'
#     feedback_message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     dietitian = models.ForeignKey(DietitianProfile, on_delete=models.SET_NULL, null=True, blank=True)
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f'{self.user.username} Feedback'

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_message', 'dietitian', 'doctor']


# models.py

from django.db import models
from django.contrib.auth.models import User

class LogMeals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()
    meal_choices = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    meal = models.CharField(max_length=10, choices=meal_choices)
    timestamp = models.DateTimeField(auto_now_add=True)



class TimeSlot(models.Model):
    session_choices = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    
    dietitian = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.CharField(max_length=20, choices=session_choices)
    time = models.CharField(max_length=50)

    def get_user(self):
        # Accessing the CustomUser instance associated with the DietitianProfile
        return self.dietitian.user if self.dietitian else None
    
    def __str__(self):
        return f"{self.session} - {self.time} - Dietitian: {self.get_user()}"



class DoctorSlot(models.Model):
    session_choices = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.CharField(max_length=20, choices=session_choices)
    time = models.CharField(max_length=50)

    def get_user(self):
        # Accessing the CustomUser instance associated with the DoctorProfile
        return self.doctor.user if self.doctor else None
    
    
    def __str__(self):
        return f"{self.session} - {self.time} - Doctor: {self.get_user()}"


class DietitianRating(models.Model):
    dietitian = models.ForeignKey(DietitianProfile, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    # rating = models.IntegerField(default=1)
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"


class DoctorRating(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    # rating = models.IntegerField(default=1)
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"

# from django.conf import settings
# from django.contrib.auth import get_user_model
# class Booking(models.Model):
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     slot_datetime = models.DateTimeField()
#     # Add other booking-related fields





from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, on_delete=models.CASCADE, blank=True,  related_name='chatmessage_thread')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # media_file = models.FileField(upload_to='media/')




class Recipe(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)  # Add this line for adding an image field
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  


  def get_absolute_url(self):
      return reverse("recipes-detail", kwargs={"pk": self.pk})

  def __str__(self):
    return self.title


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Add a description field
    video_file = models.FileField(upload_to='videos/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField()
   
    # Add any other fields you need, such as tags, etc.

    def _str_(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class FoodCategory(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_food_by_category(self):
        return Food.objects.filter(category=self).count()


class Food(models.Model):
    food_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.IntegerField(default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='food_category')

    def __str__(self):
        return f'{self.food_name} - category: {self.category}'


class Image(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='get_images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.image}'


class FoodLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Log'

    def __str__(self):
        return f'{self.user.username} - {self.food_consumed.food_name}'


class Weight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weight'

    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.entry_date}'