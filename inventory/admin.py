from django.contrib import admin
from .models import *

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name','quanty',]
    search_fields = ['name','code',]

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Supplier)
admin.site.register(Inventory,InventoryAdmin)
