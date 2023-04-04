from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from .models import Close_Box
from settings.models import Consecutive_POS

@api_view(['POST'])
def Close_Box_Total(request):
	c = Close_Box.objects.filter(active = True).last()
	c.active = False
	consecutive = Consecutive_POS.objects.last().number
	c.invoice_to = consecutive
	c.save()
	return Response(True)

@api_view(['POST'])
def Get_List_Close_Box(request):
	c = Close_Box.objects.all()
	data = [
		{
			'employee':i.employee.name,
			'open_total_box':i.open_total_box,
			'close_total_box':i.close_total_box,
			'date_open':i.date_open,
			'date_close':i.date_close,
			'invoice_from':i.invoice_from,
			'invoice_to':i.invoice_to,
			'trans':i.trans,
			'cred':i.cred,
			'efec':i.efec,
			'total':i.Utili(),
			'active':i.active
		}
		for i in c
	]
	return Response(data)

@api_view(['POST'])
def Get_Close_Box(request):
	i = Close_Box.objects.filter(active = False).last()
	data ={
		'name':i.employee.name,
		'email':i.employee.email,
		'phone':i.employee.phone,
		'open_total_box':i.open_total_box,
		'close_total_box':i.close_total_box,
		'date_open':i.date_open,
		'date_close':i.date_close,
		'invoice_from':i.invoice_from,
		'invoice_to':i.invoice_to,
		'trans':i.trans,
		'cred':i.cred,
		'efec':i.efec,
		'total':i.Utili(),
		'email_company':i.employee.company.email
	}
	return Response(data)

