from django.db import models
from company.models import Company
from employee.models import Employee
from client.models import Client
from settings.models import *
from data.models import *


class Invoice_POS(models.Model):
	consecutive = models.IntegerField()
	code = models.CharField(max_length = 150)
	description = models.CharField(max_length = 100)
	price = models.FloatField()
	tax = models.FloatField()
	discount = models.FloatField()
	quanty = models.FloatField()
	date = models.CharField(max_length = 10)
	date_expired = models.CharField(max_length = 10)
	time = models.CharField(max_length = 10)
	payment_form = models.ForeignKey(Payment_Form, on_delete = models.CASCADE)
	cancelled = models.BooleanField(default = True)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	state = models.TextField(default = "Factura Creada con éxito")
	type_sell = models.CharField(max_length = 50,null = True,blank = True)
	anulated = models.BooleanField(default = False)
	
	def __str__(self):
		return self.company.name+' | '+str(self.consecutive)

	def Base_Product(self):
		base = self.price / ( 1 + ( self.tax / 100 ))
		base_with_discount = base * (self.discount / 100)
		return float(base - base_with_discount)

	def Discount_Product(self):
		base = self.price / ( 1 + ( self.tax / 100 ))
		return float(base * (self.discount / 100))


	def Tax_Product(self):
		return float((self.Base_Product() * (self.tax / 100)) * self.quanty)

	def SubTotal_Product(self):
		return float(self.Base_Product() * self.quanty)

	def Total_Product(self):
		return float(( self.Base_Product() + (self.Tax_Product() / self.quanty)  ) * self.quanty)

class Wallet_POS(models.Model):
	invoice = models.ForeignKey(Invoice_POS, on_delete = models.CASCADE)
	cancelled = models.BooleanField(default = False)
	days_in_debt = models.IntegerField(default = 0)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	payment_form = models.CharField(max_length = 50,default="")
	employee_close = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name='employee_close')
	abono = models.FloatField(default = 0)

	def Total(self):
		return self.invoice.Total_Product() - self.abono

