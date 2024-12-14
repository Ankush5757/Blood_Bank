from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile_pic/<int:id>/', views.profile_pic, name = 'profile_pic'),
    path('update_profile/<int:id>/', views.update_profile, name='update_profile'),
    path('delete_profile_pic/<int:id>/', views.delete_profile_pic, name = 'delete_profile_pic'),
    path('profile/', views.profile, name='profile'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('requests/',views.requests, name='requests'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('blood_request/',views.blood_request, name='blood_request'),
    path('blood_donor/',views.blood_donor, name='blood_donor'),
    path('approve/<int:id>/', views.approve, name='approve'),
    path('donate_us/', views.donate_us, name='donate_us'),
    path('donation_success/<int:payment>/<str:payment_id>/', views.donation_success, name='donation_success'),
    path('filter_donors/', views.filter_donors, name='filter_donors'),
    

]