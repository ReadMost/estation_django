from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from django.utils.translation import get_language, get_language_info
from rest_framework.parsers import FileUploadParser
import datetime
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_201_CREATED,
)
from django.utils import timezone


from .models import CustomUser
from .authentication import token_expire_handler, expires_in
from .serializers import UserSigninSerializer, UserSerializer, PassengerSerializer, EmployeeSerializer, EmployeeShowSerializer
from .permissions import IsOwnerObj, IsOwner
from datetime import time, datetime
import re


@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
	signin_serializer = UserSigninSerializer(data=request.data)
	if not signin_serializer.is_valid():
		return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

	user = authenticate(
		username=signin_serializer.transform_username(signin_serializer.data['username']),
		password=signin_serializer.data['password'],
	)

	if not user:
		user = authenticate(
			username=signin_serializer.transform_username_seven(signin_serializer.data['username']),
			password=signin_serializer.data['password'],
		)
	if not user:
		return Response({'detail': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
	try:
		dev_id = signin_serializer.data['device_id']
		if dev_id:
			user.device_id = dev_id
			user.save()
			print(user.device_id)
	except:
		pass
	# this

	# TOKEN STUFF
	token, _ = Token.objects.get_or_create(user=user)

	is_expired, token = token_expire_handler(token)
	user_serialized = UserSerializer(user)
	result = {**user_serialized.data, **{
		'expires_in': expires_in(token),
		'token': token.key
	}}
	return Response(result, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def passenger_signup(request):
	serializer = PassengerSerializer(data=request.data)
	if serializer.is_valid():
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user)

		is_expired, token = token_expire_handler(token)
		user_serialized = UserSerializer(user)
		result = {**user_serialized.data, **{
			'expires_in': expires_in(token),
			'token': token.key
		}}
		return Response(result, status=HTTP_201_CREATED)
	return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def employee_signup(request):
	serializer = EmployeeSerializer(data=request.data)
	if serializer.is_valid():
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user.user)

		is_expired, token = token_expire_handler(token)
		user_serialized = EmployeeShowSerializer(user)
		result = {**user_serialized.data, **{
			'expires_in': expires_in(token),
			'token': token.key
		}}
		return Response(result, status=HTTP_201_CREATED)
	return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
