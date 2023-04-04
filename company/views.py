from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from .query_api import Query_Company


@api_view(['POST'])
def Create_Company(request):
	register = Query_Company(request.data)
	result = False
	data = {}
	value = register.Create_Company()
	if value[0]:
		data = register.Create_License()
		if data[0]:
			result = True
		else:
			result = False 
	else:
		return Response({'Result':value[0],'message':value[1]})	
	return Response(data)	


