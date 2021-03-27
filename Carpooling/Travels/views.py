from django.shortcuts import render, redirect
from django.http import request
from .forms import RideForm, RequestForm
from .models import Ride, RequestStatus, RideRequest
from User.models import User, UserCar
from django.db import connection
from django.db.models import Q
import xml.etree.ElementTree as ET

# Create your views here.
def CreateRide(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            # driver = UserCar.objects.raw(f"SELECT * FROM user_usercar WHERE driver_id IN (SELECT id FROM user_user WHERE userName = {request.user})")
            driver = UserCar.objects.filter(driver = request.user)
            print(driver)
            if not driver.exists():
                return redirect('/')
            instance.driver = driver[0]
            instance.save()
    else:
        form = RideForm()
    return render(request, 'Travels/CreateRide.html',{'form' : form})

def RideRequest_v(request):
    id1 = request.POST.get("rideId")
    ride1 = Ride.objects.filter(id = id1)[0]
    rider1 = request.user
    print(rider1)
    if request.method == "POST":
        r = RideRequest(riderId = rider1, rideId = ride1, requestStatusID = RequestStatus.objects.filter(pk = 1)[0])
        r.save()
        return redirect('/')
            
def Notification(request):
    pass

def dictfetchall(cursor): 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]


# def student_list(request):

#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM student_student WHERE age > 20")
#     r = dictfetchall(cursor)

#     print(connection.queries)

#     return render(request,'output.html',{'data': r})
