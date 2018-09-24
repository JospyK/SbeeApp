from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_id', 'status', 'total',]

admin.site.register(Order, OrderAdmin)