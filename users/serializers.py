from django.conf import settings
from rest_framework import serializers, validators
import re

from .models import CustomUser, Employee

from django.utils import timezone
import datetime

class UserSerializer(serializers.ModelSerializer):
    """
        User will be created but require confirmation
        If CONFIRMATION IS ADDED REFACTOR IS MUST HAVE

    """

    first_name = serializers.CharField(max_length=35, required=True)

    # student_type = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("username", "password", "first_name", "id", "is_passenger", "is_manager", "is_employee")
        extra_kwargs = {
            'password': {'write_only': True},
        }



class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    device_id = serializers.CharField(max_length=300, required=False)

    def transform_username(self, username):
        if re.fullmatch(r"[+]\d{11}", username):
            return "8" + username[2:]
        elif re.fullmatch(r"\d{11}", username):
            return "8" + username[1:]
        return username
    def transform_username_seven(self, username):
        if re.fullmatch(r"[+]\d{11}", username):
            return "7" + username[2:]
        elif re.fullmatch(r"\d{11}", username):
            return "7" + username[1:]
        return username

    def validate_username(self, value):
        # if not re.fullmatch(r"[+]?\d{11}", value):
        #     raise serializers.ValidationError('Incompatible format. Example (87058630921) or (+77058630921) ')
        if re.fullmatch(r"[+]\d{11}", value):
            value = "8" + value[2:]
        elif re.fullmatch(r"\d{11}", value):
            value =  "8" + value[1:]
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('More than 6 symbol')
        return value



class PassengerSerializer(serializers.ModelSerializer):
    """
        User will be created but require confirmation
        If CONFIRMATION IS ADDED REFACTOR IS MUST HAVE

    """

    first_name = serializers.CharField(max_length=35, required=True)
    last_name = serializers.CharField(max_length=35, required=True)
    # student_type = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("id" , "username", "password", "first_name","last_name")
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate_username(self, value):
        # if not re.fullmatch(r"[+]?\d{11}", value):
        #     raise serializers.ValidationError('Incompatible format. Example (87058630921) or (+77058630921) ')
        if re.fullmatch(r"[+]\d{11}", value):
            value = "8" + value[2:]
        elif re.fullmatch(r"\d{11}", value):
            value =  "8" + value[1:]
        if CustomUser.objects.filter(username=value):
            raise serializers.ValidationError('User with this username(number) already exist')
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('More than 6 symbol')
        return value


    def create(self, validated_data):

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        # set false for activation
        instance.is_active = True
        instance.save()


        return instance



class EmployeeSerializer(serializers.ModelSerializer):
    """
        User will be created but require confirmation
        If CONFIRMATION IS ADDED REFACTOR IS MUST HAVE

    """

    first_name = serializers.CharField(max_length=35, required=True)
    last_name = serializers.CharField(max_length=35, required=True)
    username = serializers.CharField(max_length=35, required=True)
    password = serializers.CharField(max_length=35, required=True)


    # student_type = serializers.CharField()

    class Meta:
        model = Employee
        fields = ("username", "password", "first_name","last_name", "salary","from_time","to_time")
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate_username(self, value):
        # if not re.fullmatch(r"[+]?\d{11}", value):
        #     raise serializers.ValidationError('Incompatible format. Example (87058630921) or (+77058630921) ')
        if re.fullmatch(r"[+]\d{11}", value):
            value = "8" + value[2:]
        elif re.fullmatch(r"\d{11}", value):
            value =  "8" + value[1:]
        if CustomUser.objects.filter(username=value):
            raise serializers.ValidationError('User with this username(number) already exist')
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('More than 6 symbol')
        return value


    def create(self, validated_data):

        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        username = validated_data.pop('username', None)
        u = CustomUser.objects.create(username=username, first_name=first_name,last_name=last_name)
        validated_data["user"] = u
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.user.set_password(password)

        instance.save()


        return instance

class EmployeeShowSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"