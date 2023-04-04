from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Close_Box_Total/$',Close_Box_Total,name="Close_Box_Total"),
		url(r'^Get_List_Close_Box/$',Get_List_Close_Box,name="Get_List_Close_Box"),
	]