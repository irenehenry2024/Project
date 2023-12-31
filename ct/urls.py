from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
   
   path('',views.index, name="index"),
   path('d_index/',views.d_index, name="d_index"),
   path('dr_index/',views.dr_index, name="dr_index"),
   path('signup/', views.signup, name="signup"),
   path('signin/', views.signin, name="signin"),
   path('dsignup/', views.dsignup, name="dsignup"),
   path('drsignup/', views.drsignup, name="drsignup"),
   path('drsignup/', views.drsignup, name="drsignup"),
   path('login/', views.login, name="login"),
   # path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
   path('loggout/', views.loggout, name="loggout"),
   # path('register/', views.register, name='register'),
   path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
   path('customers/', views.customer_list, name='customer_list'),
   path('dietitians/', views.dietitian_list, name='dietitian_list'),
   path('doctors/', views.doctor_list, name='doctor_list'),
   path('user_profile/', views.user_profile, name='user_profile'),
   path('duser_profile/', views.duser_profile, name='duser_profile'),
   path('druser_profile/', views.druser_profile, name='druser_profile'),
   path('admindashboard/', views.admindashboard, name='admindashboard'),
   path('doctors_list/', views.doctors_list, name='doctors_list'),
   path('dietitians_list/', views.dietitians_list, name='dietitians_list'),
   path('book-doctor/', views.book_doctor, name='book_doctor'),
   # path('delete-doctor/', views.delete_doctor, name='delete_doctor'),   
   path('verify_doctor/<int:doctor_id>/', views.verify_doctor, name='verify_doctor'),
   path('view_doctor_details/', views.view_doctor_details, name='view_doctor_details'),
   path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
   # path('doctor_profile/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
   path('change_password/', views.change_password, name='change_password'),
   path('change_password/', views.change_password, name='change_password'),
   path('bmi_estimation/', views.bmi_estimation, name='bmi_estimation'),
   path('recipe_catalog/', views.recipe_catalog, name='recipe_catalog'),
   path('log-exercise/', views.log_exercise, name='log_exercise'),
   path('calorie_counting/', views.calorie_counting, name='calorie_counting'),
   path('food_intake/', views.food_intake, name='food_intake'),
   path('book-dietitian/', views.book_dietitian, name='book_dietitian'),
   # path('delete-dietitian/', views.delete_dietitian, name='delete_dietitian'),   
   path('verify_dietitian/<int:dietitian_id>/', views.verify_dietitian, name='verify_dietitian'),
   path('dietitian_profile/', views.dietitian_profile, name='dietitian_profile'),
   path('decline_doctor/<int:doctor_id>/', views.decline_doctor, name='decline_doctor'),
   path('decline_dietitian/<int:dietitian_id>/', views.decline_dietitian, name='decline_dietitian'),
   path('view_dietitian_details/', views. view_dietitian_details, name=' view_dietitian_details'),
   path('logout_view/', views.logout_view, name='logout_view'),

   path('ratings/', views.ratings, name='ratings'),
   path('dietitian_ratings/<int:dietitian_id>/', views.dietitian_ratings, name='dietitian_ratings'),
   path('dietitian_ratings_page/<int:dietitian_id>/', views.dietitian_ratings_page, name='dietitian_ratings_page'),

   path('dietitian/<int:dietitian_id>/timeslots/', views.dietitian_timeslots, name='dietitian_timeslots'),
   path('dietitian_payment/<int:booking_id>/', views.dietitian_payment, name='dietitian_payment'),
   path('pay/<int:booking_id>/', views.paymenthandler, name='pay'),

   path('doctor/<int:doctor_id>/timeslots/', views.doctor_timeslots, name='doctor_timeslots'),
   path('doctor_payment/<int:booking_id>/', views.doctor_payment, name='doctor_payment'),
   path('pay/<int:booking_id>/', views.payment, name='pay'),

   path('dratings/', views.dratings, name='dratings'),
   path('doctor_ratings/<int:doctor_id>/', views.doctor_ratings, name='doctor_ratings'),
   path('doctor_ratings_page/<int:doctor_id>/', views.doctor_ratings_page, name='doctor_ratings_page'),


   
   path('dr_bookings/<int:doctor_id>/', views.dr_bookings, name='dr_bookings'),
   path('d_bookings/<int:dietitian_id>/', views.d_bookings, name='d_bookings'),

   path('log_meals/', views.log_meals, name='log_meals'),
  
   
   path('feedback_form/', views.feedback_form, name='feedback_form'),
   path('add_slot/', views.add_slot, name='add_slot'),
   path('dr_addslot/', views.dr_addslot, name='dr_addslot'),
   path('submit_feedback/dietitian/', views.submit_feedback, {'professional_type': 'dietitian'}, name='submit_dietitian_feedback'),
   path('submit_feedback/doctor/', views.submit_feedback, {'professional_type': 'doctor'}, name='submit_doctor_feedback'),

  

path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 # path('doctor/feedback/', doctor_feedback, name='doctor_feedback'),
   # path('dietitian/feedback/', dietitian_feedback, name='dietitian_feedback'),
 # path('select_availability/', views.select_availability, name='select_availability'),
   # path('select_availability/<int:dietitian_id>/', views.select_availability, name='select_availability'),

   #  path('submit_feedback/<str:professional_type>/<int:professional_id>/', views.submit_feedback, name='submit_feedback'),
   #  path('d_feedback/<int:professional_id>/', views.d_feedback, name='d_feedback'),
   #  path('dr_feedback/<int:professional_id>/', views.dr_feedback, name='dr_feedback'),
   # path('dietitian-ratings//', views.dietitian_ratings_page, name='dietitian_ratings_page'),

   # path('booked_doctors/', views.booked_doctors_list, name='booked_doctors_list'),
   # path('booked_doctor/<int:doctor_id>/', views.booked_doctor_details, name='booked_doctor_details'),
   
   # path('update_user_status/<int:user_id>/<str:new_status>/', views.update_user_status, name='update_user_status'),
   # path('loggout/', auth_views.LogoutView.as_view(), name="loggout"),
  