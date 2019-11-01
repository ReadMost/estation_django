from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _




class CustomUser(AbstractUser):
	is_passenger = models.BooleanField(default=True)
	is_manager = models.BooleanField(default=False)
	is_employee = models.BooleanField(default=False)



	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return str(self.first_name)

class Employee(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	salary = models.IntegerField(default=0, null=True, blank=True)
	from_time = models.TimeField(null=True, blank=True)
	to_time = models.TimeField(null=True, blank=True)

	def clean(self, *args, **kwargs):
		if self.user.is_manager:
			raise ValidationError(
				_('person can not be manager and employee is not an even number')

			)

	def save(self, *args, **kwargs):
		self.user.is_employee = True
		self.user.save()
		super(Employee, self).save(*args, **kwargs)

	def __str__(self):
		return "employee" + str(self.user.first_name)