# -*- coding: utf-8 -*-
from __future__ 	import unicode_literals
from django.db 		import models
from django.urls 	import reverse

class FichierManager(models.Model):
	"""docstring for FichierManager"""
	def get_by_id(self, id):
		return self.get_queryset().filter(id=id)


class Fichier(models.Model):
	nom 		= models.CharField(max_length=50,)
	lignes 		= models.IntegerField(help_text='help_text')
	montant 	= models.IntegerField(help_text='help_text')
	timestamp	= models.DateTimeField(auto_now_add=True)

	objects = FichierManager()

  
	class Meta:
		ordering = ('-timestamp',)
		# permissions = (
		# 	('VIEW_FILES', 'can view files and related stuff'),
		# )

	def get_url(self):
		return reverse('fichiers:show', kwargs={'pk': self.pk})
	
	def __str__(self):
		return self.nom

	def __unicode__(self):
		return self.nom