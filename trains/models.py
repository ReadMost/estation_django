from django.db import models


# Create your models here.
"""
Station
"""
class Station(models.Model):
	name = models.CharField(max_length=70, null=False)

'''Train'''

class Train(models.Model):
	pass

	def __str__(self):
		return str(self.pk)

'''
Schedule
'''
class Day(models.Model):
	name = models.CharField(max_length=50, null=False)

	def __str__(self):
		return self.name


class TypeSchedule(models.Model):
	day = models.ManyToManyField(Day)
	name = models.CharField(max_length=50, null=False)
	def __str__(self):
		return self.name

class Schedule(models.Model):
	type = models.ForeignKey(TypeSchedule, on_delete=models.CASCADE)
	train = models.ForeignKey(Train, on_delete=models.CASCADE)
	stations = models.ManyToManyField(Station, through="Include")
	def __str__(self):
		return "schedule" + str(self.pk)



# include station and schedule

class Include(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE)
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
	arr_time = models.TimeField()
	dep_time = models.TimeField()

	def __str__(self):
		return str(self.arr_time) + str(self.dep_time)

class Carriage(models.Model):
	TYPE = (
		("P", "Normal"),
		("L", "Luxury"),
		("S", "Super-Luxury"),
	)
	number = models.IntegerField()
	type = models.CharField(max_length=1, choices=TYPE)
	train = models.ForeignKey(Train, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.number)


class Seat(models.Model):
	number = models.IntegerField()
	carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)


	def __str__(self):
		return str(self.number)


'''Ticket'''

class Ticket(models.Model):
	price = models.IntegerField(null=False)
	document_id = models.CharField(max_length=12, null=False)
	l_name = models.CharField(max_length=50,null=False)
	f_name = models.CharField(max_length=50,null=False)
	date = models.DateTimeField(null=False)
	from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="from_station")
	to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="to_station")
	seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

	def __str__(self):
		return self.from_station + " -> " + self.to_station