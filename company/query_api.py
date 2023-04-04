from .models import *
from settings.models import *
import datetime

class Query_Company:
	def __init__(self, data):
		self.data = data

	def Create_Company(self):
		
		try:
			Company(
				nit = self.data['nit'],
				name = self.data['name'],
				address = self.data['address'],
				email = self.data['email'],
				phone = self.data['phone'],
				phone_2 = self.data['phone_2']
			).save()
			company = Company.objects.get(nit = self.data['nit'])
			Consecutive_FE(number = 1, company = company).save()
			Consecutive_POS(number = 1, company = company).save()
			Resolution_POS(
				prefix = "SETP",
				resolution = "18760000001",
				from_number = 990000000,
				to_number = 995000000,
				date_from = "2019-01-19",
				date_to = "2030-01-19",
				company = company
			).save()
			Resolution_FE(
				prefix = "SETP",
				resolution = "18760000001",
				from_number = 990000000,
				to_number = 995000000,
				date_from = "2019-01-19",
				date_to = "2030-01-19",
				company = company
			).save()
			message = "Success"
			result = True
		except Exception as e:
			print(e)
			message = str(e)
			result = False
		return [result,message]
		
	def Licenses(self):
		document_annual = 0
		user = 0

		#LOS PRECIOS SON MENSUALES
		if int(self.data['price']) == 0:# FREE 
			document_annual = 9
			user = 1
		elif int(self.data['price']) == 15000:
			document_annual = 25
			user = 1
		elif int(self.data['price']) == 22000:
			document_annual = 50
			user = 1
		elif int(self.data['price']) == 46500:
			document_annual = 500
			user = 2
		elif int(self.data['price']) == 150000:
			document_annual = 1500
			user = 5
		elif int(self.data['price']) == 166670:
			document_annual = 2300
			user = 5
		elif int(self.data['price']) == 250000:
			document_annual = 50000
			user = 50
		else:
			document_annual = 0
			user = 0

		return [document_annual,user]

	def Create_License(self):
		data = {}
		company = Company.objects.get(nit = self.data['nit'])
		try:
			today = datetime.datetime.utcnow()
			lic = self.Licenses()
			data = {
				'pk':company.pk,
				'nit' : self.data['nit'],
				'name' : self.data['name'],
				'address' : self.data['address'],
				'email' : self.data['email'],
				'phone' : self.data['phone'],
				'phone_2' : self.data['phone_2'],
				'price' : self.data['price'],
				'date_payment' : today,
				'date_experied' : today + datetime.timedelta(days=30),
				'document_annual' : lic[0],
				'usuarios' : lic[1]
			}
			License(
				price = self.data['price'],
				date_payment = today,
				dete_experied = today + datetime.timedelta(days=30),
				document_annual = lic[0],
				employee = lic[1],
				company = company
			).save()
			result = True
		except Exception as e:
			print(e)
			result = False
		return [result,data]
		





