from django.db import models
from django.urls import reverse
from comptes.models import User
from datetime import datetime

class FactureManager(models.Model):
	def get_by_id(self, id):
		return self.get_queryset().filter(id=id)

class ImpayeeManager(models.Manager):
	def get_queryset(self):
		return super(ImpayeeManager, self).get_queryset().filter(status='i')


class PayeeManager(models.Manager):
	def get_queryset(self):
		return super(PayeeManager, self).get_queryset().filter(status='p')



class Facture(models.Model):
	user_ref		= models.ForeignKey(User, null=True, related_name="user", verbose_name="Reference Abonne", on_delete=models.CASCADE)
	agence 			= models.IntegerField( help_text="AGENCE PAYEUR" , verbose_name="AGENCE PAYEUR"	)
	centre 			= models.IntegerField( help_text="CENTRE PAYEUR" , verbose_name="CENTRE PAYEUR"	)
	panneau 		= models.CharField(max_length=8, help_text="PANNEAU" , verbose_name="PANNEAU"	)
	ref 			= models.CharField(max_length=30, help_text="REFERENCE ABONNE" , verbose_name="REFERENCE ABONNE"	)
	annee_conso		= models.IntegerField( help_text="ANNEE DE CONSOMMATION" , verbose_name="ANNEE DE CONSOMMATION"	)
	periode_conso 	= models.IntegerField( help_text="PERIODE DE CONSOMMATION" , verbose_name="PERIODE DE CONSOMMATION"	)
	annee_factu		= models.IntegerField( help_text="ANNEE DE FACTURATION" , verbose_name="ANNEE DE FACTURATION"	)
	periode_factu 	= models.IntegerField( help_text="PERIODE DE FACTURATION" , verbose_name="PERIODE DE FACTURATION"	)
	montant_conso 	= models.IntegerField( help_text="MONTANT CONSOMMATION" , verbose_name="MONTANT CONSOMMATION"	)
	montant_ht 		= models.IntegerField( help_text="MONTANT HORS TAXE" , verbose_name="MONTANT HORS TAXE"	)
	nufmmr 			= models.CharField(max_length=12, help_text="digits(nufmmr)" , verbose_name="digits(nufmmr)"	)
	montant_surtaxe = models.IntegerField( help_text="MONTANT SURTAXE" , verbose_name="MONTANT SURTAXE"	)
	contribution	= models.IntegerField( help_text="CONTRIBUTION ELEC/RURALE" , verbose_name="CONTRIBUTION ELEC/RURALE"	)
	montant_ttc 	= models.IntegerField( help_text="MONTANT TTC" , verbose_name="MONTANT TTC"	)
	net_a_payer		= models.IntegerField( help_text="NET A PAYER" , verbose_name="NET A PAYER"	)
	piece_conso		= models.CharField(max_length=3, help_text="TYPE PIECE CONSOM." , verbose_name="TYPE PIECE CONSOM."	)
	taux_tva		= models.IntegerField( help_text="TAUX TVA" , verbose_name="TAUX TVA"	)
	montant_tva 	= models.IntegerField( help_text="MONTANT TVA" , verbose_name="MONTANT TVA"	)
	conso_facture	= models.IntegerField( help_text="Conso facturée" , verbose_name="Conso facturée"	)
	jours_conso		= models.IntegerField( help_text="NOMBRE JOURS CONSO" , verbose_name="NOMBRE JOURS CONSO"	)
	old_index 		= models.IntegerField( help_text="ANCIEN INDEX" , verbose_name="ANCIEN INDEX"	)
	new_index 		= models.IntegerField( help_text="NOUVEL INDEX" , verbose_name="NOUVEL INDEX"	)
	date_releve 	= models.IntegerField( help_text="DATE RELEVE" , verbose_name="DATE RELEVE"	)
	tarif 			= models.CharField(max_length=4, help_text="TARIF" , verbose_name="TARIF"	)
	date_limite 	= models.IntegerField( help_text="DATE LIMITE PAIEMENT" , verbose_name="DATE LIMITE PAIEMENT"	)
	nom_abonne 		= models.CharField(max_length=40, help_text="NOM DU PAYEUR" , verbose_name="NOM DU PAYEUR"	)
	adresse 		= models.CharField(max_length=40, help_text="ADRESSE 1" , verbose_name="ADRESSE 1"	)
	montant_lht 	= models.IntegerField( help_text="MONTANT LOCATION HT" , verbose_name="MONTANT LOCATION HT"	)
	montant_al 		= models.IntegerField( help_text="MONTANT AUTRES LOCATIONS" , verbose_name="MONTANT AUTRES LOCATIONS"	)
	status_choices 	= (('p', 'Paye'), ('i', 'Impaye'),)
	timestamp		= models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=status_choices, blank=False,default='i',help_text='Paye ou Impaye')


	objects = FactureManager()

	class Meta:
		ordering = ('-timestamp',)

	def get_url(self):
		return reverse('factures:show', kwargs={'pk': self.pk})

	@property
	def date_limitee(self):
		data = str(self.date_limite)
		data = data[6:8] + data[4:6] + data[0:4]
		data = datetime.strptime(data, '%d%m%Y')
		data = datetime.strftime(data, '%d %b %Y')
		print(data)
		return data

	@property
	def periode_factuu(self):
		data = str(self.periode_factu)
		data = datetime.strptime(data, '%m')
		data = datetime.strftime(data, '%b')
		print(data)
		return data
	
	@property
	def taxe_func(self):
		return self.montant_lht * 0.18	
	
	@property
	def montant_func(self):
		return self.montant_conso + self.montant_surtaxe + self.contribution

	
	def __str__(self):
		return self.ref

	def __unicode__(self):
		return self.ref

	def __iter__(self):
		return iter([self.ref, self.periode_factuu, self.montant_ttc])

