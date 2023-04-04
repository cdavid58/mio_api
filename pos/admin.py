from django.contrib import admin
from .models import *

class Invoice_POSAdmin(admin.ModelAdmin):
    list_display = ['code', 'description','price',]
    search_fields = ['description','code',]

admin.site.register(Invoice_POS,Invoice_POSAdmin)
admin.site.register(Wallet_POS)
