from django.shortcuts import render, redirect
from .forms import CustUserCreationForm, CustUserChangeForm, UserCarForm, LicenseForm
from django.contrib.auth import login, authenticate
from .models import UserCar
from Travels.models import Ride, RideRequest, RequestStatus
from django.db.models import Q
from django.db import connection
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def dictfetchall(cursor): 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def UserRegister(request):
	if request.method == 'POST':
		form = CustUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.userName, password=raw_password)
			login(request, user)
			if user.driverLicense is not None or user.licenseValidFrom is not None:
				print('Has drivers license')
				return redirect('/user/Add-Car')
			messages.success(request, f'Account for user {user.userName} created successfully!')
			return redirect('/')
	else:
		form = CustUserCreationForm()
	return render(request, 'User/Register.html', {'form':form})

def AddCar(request):
	driver = request.user
	if driver.driverLicense is None or driver.licenseValidFrom is None:
		return redirect('/')
	if request.method == 'POST':
		form = UserCarForm(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.driver = driver
			instance.save()
			return redirect('/')
	else:
		form = UserCarForm()
	
	return render(request, 'User/Driver.html', {'form' : form})

def UserRide(request):
	user = request.user
	if(UserCar.objects.filter(driver=request.user)):
		cursor = connection.cursor()
		cursor.execute("SELECT * from travels_ride where driver_id in (select id from user_usercar where driver_id = %s)",[request.user.id])
		rides = dictfetchall(cursor)
		print(connection.queries)
		# driver = UserCar.objects.filter(driver=request.user)[0]
		# rides = Ride.objects.filter(driver=driver)
		cursor2 = connection.cursor()
		cursor2.execute("select user_user.userName,travels_riderequest.* from travels_riderequest inner join user_user on travels_riderequest.riderId_id=user_user.id where travels_riderequest.requestStatusId_id=1 and travels_riderequest.rideId_id in (select id from travels_ride where driver_id in (select id from user_usercar where driver_id = %s));",[request.user.id])
		riderequests = dictfetchall(cursor2)
		print(connection.queries)
		# riderequests = RideRequest.objects.filter()
		# pending = RequestStatus.objects.filter(pk = 1)[0]
		return render(request, 'Travels/myRidesDetails.html', {'rides': rides, 'requests': riderequests})
	else:
		print("No rides to show.")
		return redirect('/')

def AddLicense(request):
	user = request.user
	if request.method == 'POST':
		form = LicenseForm(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user.driverLicense = instance.driverLicense
			user.licenseValidFrom = instance.licenseValidFrom
			user.save()
			return redirect('/user/Add-Car')
	else:
		form = LicenseForm()
	return render(request, 'User/licensedeets.html', {'form':form})

def UserProfile(request):
	user = request.user
	userPassenger = RideRequest.objects.filter(riderId = user).filter(requestStatusID__id = 2)
	userPassengerPend = RideRequest.objects.filter(riderId = user).filter(requestStatusID__id = 1)
	print(userPassengerPend)
	print(userPassenger)
	context = {}
	if(UserCar.objects.filter(driver=request.user)):
		cursor = connection.cursor()
		cursor.execute("SELECT * from travels_ride where driver_id in (select id from user_usercar where driver_id = %s)",[request.user.id])
		userRide = dictfetchall(cursor)
		# userPassenger = Ride.objects.filter(riderequest__riderId = user).filter(riderequest__requestStatusID__description = 'Accepted')
		# userPassengerPend = Ride.objects.filter(riderequest__riderId = user).filter(riderequest__requestStatusID__description = 'Pending')
		Passengers = RideRequest.objects.filter(rideId__driver__driver = user).filter(requestStatusID__description = 'Accepted')
	# driver = UserCar.objects.filter(driver=user)
	# if driver.exists():
	# 	ride = Ride.objects.filter(driver=driver[0])
	# else:	
	# 	return render(request,'User/Profile.html', {'user' : user})
		context = {'user':user, 'rides' : userRide, 'userPassengers' : userPassenger,  'Passengers' : Passengers, 'userPassengersPend' : userPassengerPend}
		return render(request,'User/Profile.html',context)
	context = {'user':user, 'userPassengers' : userPassenger, 'userPassengersPend' : userPassengerPend}
	# print(context['userPassengers'])
	return render(request,'User/Profile.html',context)

# ride = Ride.objects.filter(
# 			~Q(driver__driver = user)).filter(
# 			~Q(riderequest__riderId = user)).filter(
# 			startDate__gte=timezone.now())

def Search(request):
	user = request.user
	if request.method=='GET':
		q = request.GET.get('q')
		p = request.GET.get('p')
		if(UserCar.objects.filter(driver=request.user)):
			driver = UserCar.objects.filter(driver = request.user)[0]
			rides = Ride.objects.filter(startingPoint__icontains=q,endingPoint__icontains=p).filter(
			~Q(driver__driver = user)).filter(
			~Q(riderequest__riderId = user)).filter(
			startDate__gte=timezone.now())
		else:
			rides = Ride.objects.filter(startingPoint__icontains=q,endingPoint__icontains=p).filter(
			~Q(riderequest__riderId = user)).filter(
			startDate__gte=timezone.now())
		return render(request, 'User/Home.html',{'rides': rides, 'q': q, 'p':p})
	else:
		return HttpResponse('Please submit a search term.')

def About(request):
	return render(request,'User/About.html')
