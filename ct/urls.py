from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

from django.urls import path
from .views import display_videos

'app/model_viewtype'
'recipes/recipe_detail.html'


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
   path('messages_page/', views.messages_page, name="messages_page"),
   
   path('recipes/home', views.RecipeListView.as_view(), name="recipes-home"),
   path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
   path('recipes/create', views.RecipeCreateView.as_view(), name="recipes-create"),
   path('recipes/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
   path('recipes/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
  #  path('about/', views.about, name="recipes-about"),


  path('dashboard/', views.dashboard, name="dashboard"),
  path('d_dashboard/', views.d_dashboard, name="d_dashboard"),
  path('upload_video/', views.upload_video, name='upload_video'),
  path('display_videos/', views.display_videos, name='display_videos'),
  path('strategy_index/', views.strategy_index, name='strategy_index'),

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
   path('view_recipes/', views.view_recipes, name='view_recipes'),

   
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
   path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),

   
   path('dr_bookings/<int:doctor_id>/', views.dr_bookings, name='dr_bookings'),
   path('d_bookings/', views.d_bookings, name='d_bookings'),
   path('add_slot/', views.add_slot, name='add_slot'),
   path('dr_addslot/', views.dr_addslot, name='dr_addslot'),


    path('indexfood/', views.indexfood, name='indexfood'),
    path('profile/weight', views.weight_log_view, name='weight_log'),
    path('profile/weight/delete/<int:weight_id>', views.weight_log_delete, name='weight_log_delete'),
    path('food/list', views.food_list_view, name='food_list'),
    path('food/add', views.food_add_view, name='food_add'),
    path('food/foodlog', views.food_log_view, name='food_log'),
    path('food/foodlog/delete/<int:food_id>', views.food_log_delete, name='food_log_delete'),
    path('food/<str:food_id>', views.food_details_view, name='food_details'),
    path('categories', views.categories_view, name='categories_view'),
    path('categories/<str:category_name>', views.category_details_view, name='category_details_view'),

    path('calldashboard/',views.calldashboard, name='calldashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('join/',views.join_room, name='join_room'),
    path('recommend_recipes/', views.recommend_recipes, name='recommend_recipes'),
  

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
  