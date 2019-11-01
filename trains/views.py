from django.shortcuts import render
from .serializers import FindByDate, StationListSerializer, TrainSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Schedule, Station, Include
from rest_framework.response import Response
from rest_framework import generics
import datetime
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_201_CREATED,
)
# Create your views here.

@api_view(["POST"])
@permission_classes((AllowAny,))
def find_by_name(request):
	ser = FindByDate(data = request.data)

	if ser.is_valid():
		print(ser.validated_data)
		date = ser.validated_data['date']
		from_city = ser.validated_data['from_city']
		to_city = ser.validated_data['to_city']
		schedules = Schedule.objects.filter(type__name__icontains=date.weekday(), stations__in= (from_city, to_city) )
		trains = set()
		for i in schedules:
			if Include.objects.get(schedule = i, station=from_city).arr_time < Include.objects.get(schedule = i, station=to_city).arr_time:
				trains.add(i.train)

		return Response(TrainSerializer(trains, many=True).data)
	else:
		return Response(ser.errors)

class StationList(generics.ListAPIView):
	serializer_class = StationListSerializer
	permission_classes = [AllowAny]
	queryset = Station.objects.all()

