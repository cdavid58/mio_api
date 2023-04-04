from django.db import models
from company.models import Company

class Category(models.Model):
	name = models.CharField(max_length = 150)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 150)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Supplier(models.Model):
	nit = models.IntegerField(null= True, blank=True)
	name = models.CharField(max_length = 150)
	phone = models.CharField(max_length = 15, null = True, blank = True)
	email = models.EmailField(null = True, blank = True)
	address = models.CharField(max_length= 150,null = True, blank = True)


class Inventory(models.Model):
	code = models.CharField(max_length = 300)
	name = models.CharField(max_length = 150)
	quanty = models.FloatField()
	und = models.IntegerField(default = 0)
	metro = models.IntegerField(default = 0)
	und_static = models.IntegerField(default = 0)
	metro_static = models.IntegerField(default = 0)
	tax = models.IntegerField(default=0)
	cost = models.FloatField()
	price_1 = models.FloatField()
	price_2 = models.FloatField(null = True, blank = True)
	price_3 = models.FloatField(null = True, blank = True)
	price_4 = models.FloatField(null = True, blank = True)
	price_5 = models.FloatField(null = True, blank = True)
	supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
	company = models.ForeignKey(Company,on_delete = models.CASCADE)

	def __str__(self):
		return self.name+' | '+self.company.name



