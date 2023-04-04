from invoice.models import Invoice_FE, Wallet_FE
from pos.models import Invoice_POS, Wallet_POS
from company.models import Company, License
from employee.models import Employee
from client.models import Client
from data.models import Payment_Form
from inventory.models import Inventory
from settings.models import *
from close_box.models import Close_Box
import json

class Create_Invoice:
	def __init__(self,data):
		self.data = data
		self.value = None
		if int(self.data[0]['type']) == 1:
			self.value = self.Create_Invoice_FE()
		else:
			self.value =  self.Create_Invoice_POS()

	def Discount_Inventory(self,quanty,code,type_sell):
		inventory = Inventory.objects.get(code = str(code))
		if str(type_sell) == "Unidad":
			inventory.und -= int(quanty)
			inventory.save()
			if inventory.und == 0:
				if inventory.quanty > 0:
					inventory.und = inventory.und_static
					inventory.quanty -= 1
					inventory.save()
		if str(type_sell) == "Metros":
			inventory.metro -= int(quanty)
			inventory.save()
			if inventory.metro == 0:
				if inventory.quanty > 0:
					inventory.metro = inventory.metro_static
					inventory.quanty -= 1
					inventory.save()
		elif str(type_sell) == 'Completo':
			print(quanty)
			if inventory.quanty > 0:
				inventory.quanty -= int(quanty)

		inventory.save()

	def Create_Invoice_FE(self):
		company = Company.objects.get(pk = self.data[0]['company'])
		consecutive = Consecutive_FE.objects.get(company = company)
		license = License.objects.get(company = company)
		if license.document_annual >= 1:
			for i in self.data:
				price = float(i['VAL. UNIT'])
				tax = i['IVA'].replace('%','')
				Invoice_FE(
					consecutive = consecutive.number,
					code = str(i['CODIGO']).strip(),
					description = i['DESCRIPCION'],
					price = price,
					tax = tax,
					discount = i['VAL. DESC.'],
					quanty = i['CANTIDAD'],
					date = self.data[0]['date'],
					date_expired = self.data[0]['date_expired'],
					time = self.data[0]['time'],
					payment_form = Payment_Form.objects.get(pk = self.data[0]['payment_form']),
					cancelled = self.data[0]['cancelled'],
					employee = Employee.objects.get(pk = self.data[0]['employee']),
					client = Client.objects.get(pk = self.data[0]['client']),
					company = Company.objects.get(pk = self.data[0]['company']),
					type_sell = i['TIPO DE VENTA']
				).save()
				self.Discount_Inventory(i['CANTIDAD'],i['CODIGO'],i['TIPO DE VENTA'])
			invoice = Invoice_FE.objects.filter(consecutive = consecutive.number)
			if not self.data[0]['cancelled']:
				Wallet_FE(
					invoice = invoice,
					company = invoice.company
				).save()
			total= 0

			for i in invoice:
				total += i.Total_Product()
			data = {
				'result':True,
				"pk": invoice.last().pk,
				"consecutive": consecutive.number,
				"client": invoice.last().client.name,
				"total": total,
				"state":invoice.last().state,
			}
			del invoice
			consecutive.number += 1
			consecutive.save()
			license.document_annual -= 1
			license.save()
		else:
			data = {'result':False}
		return data

	def Create_Invoice_POS(self):
		consecutive = Consecutive_POS.objects.last()
		company = Company.objects.get(pk = self.data[0]['company'])
		information_payment = self.data[0]
		try:
			data = True
			forma = None
			for i in self.data:
				price = float(i['VAL. UNIT'])
				tax = i['IVA'].replace('%','')
				quanty = int(str(i['CANTIDAD']).strip().replace('-',''))
				Invoice_POS(
					consecutive = consecutive.number,
					code = str(i['CODIGO']).strip(),
					description = i['DESCRIPCION'],
					price = price,
					tax = tax,
					discount = i['VAL. DESC.'],
					quanty = quanty,
					date = self.data[0]['date'],
					date_expired = self.data[0]['date_expired'],
					time = self.data[0]['time'],
					payment_form = Payment_Form.objects.get(pk = self.data[0]['payment_form']),
					cancelled = self.data[0]['cancelled'],
					employee = Employee.objects.get(pk = self.data[0]['employee']),
					client = Client.objects.get(pk = self.data[0]['client']),
					company = Company.objects.get(pk = self.data[0]['company']),
					type_sell = i['TIPO DE VENTA']
		         ).save()
				forma = Payment_Form.objects.get(pk = self.data[0]['payment_form']).name
				self.Discount_Inventory(quanty,i['CODIGO'],i['TIPO DE VENTA'])
			invoice = Invoice_POS.objects.filter(consecutive = consecutive.number)
			if not self.data[0]['cancelled']:
				Wallet_POS(
					invoice = invoice.last(),
					company = Company.objects.get(pk = self.data[0]['company']),
					days_in_debt = self.data[0]['days_expired'],
					employee = Employee.objects.get(pk = self.data[0]['employee'])
		        ).save()

			total= 0
			for i in invoice:
				total += i.Total_Product()
			data = {
				"pk": invoice.last().pk,
				"consecutive": consecutive.number,
				"client": invoice.last().client.name,
				"total": total,
				'result':True
			}
			del invoice
			consecutive.number += 1
			consecutive.save()
			license = License.objects.get(company = company)
			license.document_annual -= 1
			license.save()
			close_box = Close_Box.objects.filter(active=True).last()

			close_box.close_total_box += total
			if int(self.data[0]['payment_form']) == 2:
				close_box.payment_form = 'Credito'
				close_box.cred += total
			elif int(self.data[0]['payment_form']) == 3:
				close_box.payment_form = 'Consignacion'
				close_box.trans += total
			elif int(self.data[0]['payment_form']) == 4:
				close_box.payment_form = 'Mixto'
				close_box.efec += int(self.data[0]['efectivo'])
				close_box.trans += int(self.data[0]['transferencia'])
			else:
				close_box.payment_form = 'Efectivo'
				close_box.efec += total
			close_box.save()
		except Exception as e:
		    data = str(e)
		    print(e,'error')
		return data


