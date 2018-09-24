from django.contrib import admin
from .models import Facture


class FactureAdmin(admin.ModelAdmin):
	list_display = ['user_ref',  ]
	#fields = []

admin.site.register(Facture, FactureAdmin)