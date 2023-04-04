from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from create_invoice import Create_Invoice
import json, sqlite3, time
from client.models import Client
from .models import Invoice_FE
from send_dian import SEND_DIAN
from pos.models import Invoice_POS
from company.models import Company
from settings.models import *
from inventory.models import Inventory

@api_view(['POST'])
def CREATE_INVOICE(request):
	data = request.data
	print(data,'DATA JS')
	c = Create_Invoice(data)
	result = c.value
	del c
	return Response(result)


@api_view(['POST'])
def GET_LIST_INVOICE(request):
	try:
	    data = request.data
	    conn = sqlite3.connect('/home/apiferre/apiferre/db.sqlite3')
	    cur = conn.cursor()
	    query = "invoice_invoice_fe"
	    type_invoice = int(data['type'])
	    if type_invoice == 2:
	        query = "pos_invoice_pos"
	    data = cur.execute("select DISTINCT consecutive from "+query+" where company_id = "+str(data['company'])+" order by consecutive desc limit 600").fetchall()
	    _data = []
	    start = time.time()
	    for i in data:
	        if type_invoice == 2:
	            invoice = Invoice_POS.objects.filter(consecutive = i[0])
	        else:
	            invoice = Invoice_FE.objects.filter(consecutive = i[0])
	        print(invoice)
	        total = 0
	        for j in invoice:
	            total += j.Total_Product()
	        _data.append(
	            {
	                'pk':invoice.last().pk,
	                'consecutive':i[0],
	                'client':invoice.last().client.name,
	                'total': total,
	                "state":invoice.last().state,
	                'date':invoice.last().date,
	                'cufe':invoice.last().cufe if type_invoice == 1 else None
	                }
	        )
	        total = 0
	    print(time.time() - start)
	except Exception as e:
	    _data = str(e)
	    print(e)
	return Response(_data)

@api_view(['POST'])
def GET_INVOICE(request):
	data = request.data
	query = Invoice_FE
	if data['type_invoice'] == 2:
		query = Invoice_POS
	try:
		company = Company.objects.get(pk = data['company'])
	except Company.DoesNotExist:
		company = None
	_data = {}
	if company is not None:

		invoice = query.objects.filter(consecutive = data['consecutive'],company = company)
		_data['product'] = [
			{
				'description':i.description,
				'quanty':i.quanty,
				'price_base':i.Base_Product(),
				'tax':i.tax,
				'val_tax':i.Tax_Product(),
				'discount':i.discount,
				'subtotal':i.SubTotal_Product(),
				'total':i.Total_Product(),
				'discount_product':i.Discount_Product()
			}
			for i in invoice
		]

		invoice = invoice.last()
		_data['information'] = {
			'date':invoice.date,
			'date_expired':invoice.date_expired,
			'consecutive':invoice.consecutive,
			'payment_form':invoice.payment_form.name,

		}

		client = invoice.client
		_data['client'] = {
			'name':client.name,
			'phone':client.phone,
			'email':client.email,
			'address':client.address
		}

	return Response(_data)

@api_view(['POST'])
def Send_DIAN(request):
	data = request.data
	inv = Invoice_FE.objects.filter(consecutive = data['consecutive'])
	sd = SEND_DIAN(inv)
	return Response({'Result':sd.Operations(1)})


@api_view(['POST'])
def NOTE_CREDIT_FE(request):
	data = request.data
	inv = Invoice_FE.objects.filter(consecutive = data['consecutive'])
	sd = SEND_DIAN(inv)
	return Response({'Result':sd.Operations(4)})


@api_view(['POST'])
def Delete_Invoice(request):
	data = request.data
	query = Invoice_FE
	company = Company.objects.get(pk = data['company'])
	if data['type_invoice'] == 2:
		query = Invoice_POS
	query.objects.filter(company = company, consecutive = data['consecutive']).delete()

@api_view(['POST'])
def GET_CONSECUTIVE(request):
	data = request.data
	if data['type_invoice'] == 1:
		query = Consecutive_FE.objects.get(company = data['company']).number
	else:
		query = Consecutive_POS.objects.get(company = data['company']).number

	return Response({'consecutive':query})

@api_view(['POST'])
def CLEAN_FILE(request):
	data = request.data
	invoice = Invoice_FE.objects.filter(consecutive = data['consecutive']).last()
	invoice.state = data['state']
	invoice.save()
# 	with open("./static/earring.json","w") as file:
# 		json.dump([], file, indent=4)
	return Response({'Result':True})

@api_view(['POST'])
def DELETE_INVOICE(request):
	data = request.data
	result = False
	try:
		invoice = Invoice_FE.objects.filter(consecutive = data['consecutive'],company = Company.objects.get(pk = data['company']))
		if int(data['type_invoice']) == 2:
			invoice = Invoice_POS.objects.filter(consecutive = data['consecutive'],company = Company.objects.get(pk = data['company']))
		if invoice:
			for i in invoice:
				i.delete()
			result = True
	except Exception as e:
		print(e)
	return Response({'result':result})


@api_view(['POST'])
def CreditNote(request):
	data = request.data
	invoice = None
	if int(data['type_invoice']) == 1:
		invoice = Invoice_FE.objects.filter(consecutive = data['consecutive'])
	else:
		invoice = Invoice_POS.objects.filter(consecutive = data['consecutive'])
	for i in invoice:
		inventory = Inventory.objects.get(code = i.code, company= i.company)
		inventory.quanty += i.quanty
		inventory.save()
		i.state = "Se aplico nota crédito"
		i.anulated = True
		i.save()
	return Response({'result':True})

@api_view(['POST'])
def Get_List_Note_Credit(request):
	try:
	    data = request.data
	    conn = sqlite3.connect('/home/apiferre/apiferre/db.sqlite3')
	    cur = conn.cursor()
	    query = "invoice_invoice_fe"
	    type_invoice = int(data['type'])
	    if type_invoice == 2:
	        query = "pos_invoice_pos"
	    data = cur.execute("select DISTINCT consecutive from "+query+" where anulated = True order by consecutive desc limit 600").fetchall()
	    _data = []
	    start = time.time()
	    for i in data:
	        if type_invoice == 2:
	            invoice = Invoice_POS.objects.filter(consecutive = i[0])
	        else:
	            invoice = Invoice_FE.objects.filter(consecutive = i[0])
	        print(invoice)
	        total = 0
	        for j in invoice:
	            total += j.Total_Product()
	        _data.append(
	            {
	                'pk':invoice.last().pk,
	                'consecutive':i[0],
	                'client':invoice.last().client.name,
	                'total': total,
	                "state":invoice.last().state,
	                'date':invoice.last().date,
	                'cufe':invoice.last().cufe if type_invoice == 1 else None
	                }
	        )
	        total = 0
	    print(time.time() - start)
	except Exception as e:
	    _data = str(e)
	return Response(_data)

# @api_view(['POST'])
# def Update_Wallet_POS(request):
# 	data = request.data
# 	wallet = Wallet_POS.objects.filter(invoice = Invoice_POS.objects.filter(consecutive = data['consecutive']).last())
# 	wallet.payment_form = data['payment_form']
# 	wallet.employee_close = Employee.objects.get(pk = data['pk_employee'])
# 	wallet.cancelled = True
# 	wallet.save()
# 	return Response({'result':True})


