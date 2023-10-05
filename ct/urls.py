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
   path('admindashboard/', views.admindashboard, name="admindashboard"),
   path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
   path('loggout/', auth_views.LogoutView.as_view(), name="loggout"),
  

   path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),







]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
