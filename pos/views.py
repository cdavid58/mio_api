from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from .models import *

@api_view(['POST'])
def Get_Invoice_Credit(request):
    try:
    	wallet = Wallet_POS.objects.filter(cancelled = False)
    	data = [
    		{
    			'pk':i.pk,
    			'number_invoice':i.invoice.consecutive,
    			'client':i.invoice.client.name,
    			'total':i.invoice.Total_Product(),
    			'employee':i.employee.name,
    			'days_in_debt':i.days_in_debt,
    			'date_expired':i.invoice.date_expired,
    			"cancelled":i.cancelled,
    			'total_pago':i.Total()
    		}
    		for i in wallet
    	]
    	print(data)
    except Exception as e:
        data = str(e)
    return Response(data)

@api_view(['POST'])
def Update_Wallet_POS(request):
	data = request.data
	wallet = Wallet_POS.objects.get(invoice = Invoice_POS.objects.filter(consecutive = data['consecutive']).last())
	wallet.payment_form = data['payment_form']
	wallet.employee_close = Employee.objects.get(pk = data['pk_employee'])
	wallet.cancelled = True
	wallet.save()
	return Response({'result':True})


@api_view(['POST'])
def Abonar(request):
	data = request.data
	wallet = Wallet_POS.objects.get(invoice = Invoice_POS.objects.filter(consecutive = data['consecutive']).last())
	wallet.abono = data['price']
	wallet.save()
	return Response({'result':True})