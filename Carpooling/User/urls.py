from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("Registeration/",  UserRegister, name="register"),
    path('Add-Car/', AddCar, name='add_car'),
    path('Profile/',UserProfile, name='Profile'),
    path('Add-License/', AddLicense, name='Add_license'),
    path('My-Rides/',UserRide, name='My_rides'),
    re_path(r'search/',Search)
]
