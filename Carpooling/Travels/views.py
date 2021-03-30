from django.shortcuts import render, redirect
from django.http import request
from .forms import RideForm, RequestForm
from .models import Ride, RequestStatus, RideRequest
from User.models import User, UserCar
from django.db import connection
from django.db.models import Q
import xml.etree.ElementTree as ET
from django.contrib import messages

def CheckRideClash(user, startDate, endDate):
    driver = UserCar.objects.filter(driver = user)
    userPassenger = Ride.objects.filter(riderequest__riderId = user).filter(~Q(riderequest__requestStatusID = 3))
    if driver.exists(): 
        userDriver = Ride.objects.filter(driver = driver[0])
    # userPassenger = Ride.objects.filter(riderequest__riderId = user).filter(~Q(riderequest__requestStatusID = 3))
        userRides = (userDriver | userPassenger)
    else:
        userRides = userPassenger
    if userRides.exists():
        # startDate = instance.startDate
        # print(request.POST)
        # endDate = instance.endDate
        for userRide in userRides:
            if (userRide.startDate < startDate and userRide.endDate > startDate and userRide.endDate < endDate):
                # messages.warning(request, 'Ride NOT created! This ride clashes with your previous ride(s)')
                print('1')
                print(userRide)
                return 1
            if (userRide.startDate >= startDate and userRide.endDate <= endDate):
                # messages.warning(request, 'Ride NOT created! This ride clashes with your previous ride(s)')
                print('2')
                print(userRide)
                return 2
            if (userRide.startDate >= startDate and userRide.startDate <= endDate):
                # messages.warning(request, 'Ride NOT created! This ride clashes with your previous ride(s)')
                print('3')
                print(userRide)
                return 3
    
    return 4


def CreateRide(request):
    driver = UserCar.objects.filter(driver = request.user)
    if not driver.exists():
        return redirect('/user/Add-License/')
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            x = CheckRideClash(request.user, instance.startDate, instance.endDate)
            if x == 1 or x == 2 or x == 3:
                messages.warning(request, 'Ride NOT created! This ride clashes with your previous ride(s)')
                return redirect('/')
            # if instance.startDate > instance.endDate:
                # messages.warning(request, 'Starting Date cant be ')
            instance.driver = driver[0]
            instance.save()
            messages.success(request, f'Ride from {instance.startingPoint} to {instance.endingPoint} created successfully')
            return redirect('/')
    else:
        form = RideForm()
    return render(request, 'Travels/CreateRide.html',{'form' : form})

def RideRequest_v(request):
    id1 = request.POST.get("rideId")
    ride1 = Ride.objects.filter(id = id1)[0]
    rider1 = request.user
    # print(rider1)
    if request.method == "POST":
        r = RideRequest(riderId = rider1, rideId = ride1, requestStatusID = RequestStatus.objects.filter(pk = 1)[0])
        x = CheckRideClash(request.user, r.rideId.startDate, r.rideId.endDate)
        if x == 1 or x == 2 or x == 3:
            messages.warning(request, 'Ride NOT requested! This ride clashes with your previous ride(s)')
            return redirect('/')
        r.save()
        messages.success(request, f'Ride successfully requested to driver {ride1.driver.driver.userName}! Current status : PENDING.')
        return redirect('/')

def CheckStatus(request):
    user = request.user
    # cursor = connection.cursor()
    # cursor.execute("SELECT travels_requeststatus.description as description,user_user.userName as name,travels_riderequest.* from travels_riderequest inner join travels_requeststatus on travels_requeststatus.id = travels_riderequest.requestStatusID_id where travels_riderequest.riderId_id = %s and user_user.id in (select driver_id from user_usercar where id in (select driver_id from travels_ride where id in (select rideId_id from travels_riderequest where riderId_id = %s)))",tuple([request.user.id,request.user.id]))
    # rider = dictfetchall(cursor)
    rider = RideRequest.objects.filter(riderId = user)
    return render(request, 'Travels/RideStatus.html', {'rider' : rider})

def RequestAccept(request):
    request_id = request.POST.get("reqId")
    req = RideRequest.objects.filter(id = request_id)[0]
    if request.method == "POST":
        req.requestStatusID = RequestStatus.objects.filter(pk = 2)[0]
        print("Accepted")
        messages.success(request, f'Ride successfully accepted with {req.riderId.userName}!')
        req.save()
        return redirect('/')
    pass

def RequestReject(request):
    request_id = request.POST.get("reqId")
    req = RideRequest.objects.filter(id = request_id)[0]
    if request.method == "POST":
        req.requestStatusID = RequestStatus.objects.filter(pk = 3)[0]
        print("Rejected")
        messages.success(request, f'Ride successfully rejected with {req.riderId.userName}!')
        req.save()
        return redirect('/')
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
