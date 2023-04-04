from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Get_Invoice_Credit/$',Get_Invoice_Credit,name="Get_Invoice_Credit"),
		url(r'^Update_Wallet_POS/$',Update_Wallet_POS,name="Update_Wallet_POS"),
	]