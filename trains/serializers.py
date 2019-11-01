from django.conf import settings
from rest_framework import serializers, validators
from django.utils import timezone
from .models import *
import re



class StationListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Station
		fields = "__all__"

class FindByDate(serializers.Serializer):
	date = serializers.DateTimeField(required=True)
	from_city = serializers.PrimaryKeyRelatedField(required=True ,queryset=Station.objects.all())
	to_city = serializers.PrimaryKeyRelatedField(required=True, queryset=Station.objects.all())
	def validated_date(self,value):
		if value < timezone.now():
			raise serializers.ValidationError("In the past")

class ScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Schedule
		fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Seat
		fields = ("id", "number")

class CarriageSerializer(serializers.ModelSerializer):
	seats = serializers.SerializerMethodField()
	class Meta:
		model = Carriage
		fields = "__all__"

	def get_seats(self, value):
		return SeatSerializer(value.seat_set.all(), many=True).data

class TrainSerializer(serializers.ModelSerializer):
	carriages = serializers.SerializerMethodField()
	class Meta:
		model = Train
		fields = "__all__"
	def get_carriages(self, value):
		return SeatSerializer(value.carriage_set.all(), many=True).data