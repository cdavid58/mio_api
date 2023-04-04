from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from data.models import *
from company.models import Company,License

@api_view(['POST'])
def Discount_Document(request):
	data = request.data
	license = License.objects.get(company = Company.objects.get(pk = data['company']))
	result = False
	if license.document_annual > 0:
		license.document_annual -= 1
		license.save()
		result = True
	return Response({'result':result})





@api_view(['POST'])
def Type_DocumentI(request):
	data = [
		{
			'pk':i._id,
			'name':i.name
		}
		for i in Type_Document_Identification.objects.all()
	]
	return Response(data)



@api_view(['POST'])
def Type_Organizations(request):
	data = [
		{
			'pk':i._id,
			'name':i.name
		}
		for i in Type_Organization.objects.all()
	]
	return Response(data)



@api_view(['POST'])
def Type_Regimen(request):
	data = [
		{
			'pk':i._id,
			'name':i.name
		}
		for i in Type_Regime.objects.all()
	]
	return Response(data)


@api_view(['POST'])
def Municipalitys(request):
	data = [
		{
			'pk':i._id,
			'name':i.name
		}
		for i in Municipality.objects.all()
	]
	return Response(data)

@api_view(['POST'])
def Type_Documents(request):
	data = [
		{
			'pk':i._id,
			'name':i.name
		}
		for i in Type_Document.objects.all()
	]
	return Response(data)