from django.db import models
from employee.models import Employee

class Close_Box(models.Model):
	employee = models.ForeignKey(Employee, on_delete = models.CASCADE)
	open_total_box = models.FloatField(default = 450000)
	close_total_box = models.FloatField(default = 0)
	date_open = models.CharField(max_length = 12)
	date_close = models.CharField(max_length = 12)
	invoice_from = models.IntegerField(default = 0)
	invoice_to = models.IntegerField(default = 0)
	active = models.BooleanField(default = True)
	payment_form = models.CharField(max_length = 25,null=True,blank=True)
	trans = models.FloatField(default = 0)
	efec = models.FloatField(default = 0)
	cred = models.FloatField(default = 0)

	def __str__(self):
	    return str(self.close_total_box)

	def Utili(self):
		if self.close_total_box > self.open_total_box:
			return self.close_total_box - self.open_total_box
		return 0
