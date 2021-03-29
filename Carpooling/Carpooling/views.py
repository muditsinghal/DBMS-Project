from django.http import HttpResponse
from django.shortcuts import render
from Travels.models import Ride, RideRequest
from User.models import UserCar
from django.db.models import Q
from django.utils import timezone

def HomePage(request):
	user = request.user
	print(request.body)
	if request.user.is_authenticated:
		# ride = RideRequest.objects.filter(~Q(riderId = user)).filter(~Q(rideId__driver__driver = user))
		ride = Ride.objects.filter(
			~Q(driver__driver = user)).filter(
			~Q(riderequest__riderId = user)).filter(
			startDate__gte=timezone.now())
		# driver = UserCar.objects.filter(driver = request.user)
		# if driver.exists():
		# 	ride = Ride.objects.filter(~Q(driver=driver[0]))
		# else:	
		# 	ride = Ride.objects.all()
		context = {'title' : 'Home', 'rides' : ride}
		return render(request,'User/Home.html',context)
	else:
		return render(request, 'User/Home.html')

def UserLogin(request):
	pass
