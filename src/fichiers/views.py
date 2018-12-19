# -*- coding: utf-8 -*-
from __future__ 				import print_function
from django.views.generic 		import ListView, DetailView
from django.shortcuts 			import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template 			import RequestContext
from django.conf				import settings
from django.template 			import RequestContext
from django.http 	 			import HttpResponse
from factures.models 			import Facture
from comptes.models 			import User
from .models 					import Fichier
from .tasks						import *
from django.contrib.auth.decorators import login_required
import os, sys
import lzma as xz
import pandas as pd
import datetime
import time
import csv


FILE_ROOT = getattr(settings, 'FILE_ROOT')

class FichierListView(LoginRequiredMixin, ListView):
	queryset = Fichier.objects.all()
	template_name = "fichiers/list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(FichierListView, self).get_context_data(*args, **kwargs)

		#Recuperer et charger le fichier -----------------------------------------
		date = datetime.datetime.now().strftime("%d-%m-%y")
		filename = 'facture_{}.csv'.format(date)
		file_ = os.path.join(FILE_ROOT, filename)

		if os.path.exists(file_):
			readed = pd.read_csv(file_, usecols=[9,], names=['montant'] , header=None, encoding='cp850')
			readed2 = readed.sum().to_dict()
			details = {
				'filename': filename,
				'lignes': readed.size,
				'montant' : readed2['montant']
			}
			context={ 'details' : details, }
		else:
			print('Le fichier', filename, end=' n\'existe pas.\n ')

		context.update({'fichier_list' : Fichier.objects.all()})
		print(Fichier.objects.all())
		return context



class FichierDetailView(LoginRequiredMixin, DetailView):
	#queryset = Fichier.objects.all()
	template_name = "fichiers/details.html"

	def get_context_data(self, *arg, **kwargs):
		context = super(FichierDetailView, self).get_context_data(*arg, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context["cart"] = cart_obj
		return context



def loaddt(request):
	start_time = time.time()
	#Recuperer et charger le fichier -----------------------------------------
	date = datetime.datetime.now().strftime("%d-%m-%y")
	filename = 'facture_{}.csv'.format(date)
	file_ = os.path.join(FILE_ROOT, filename)

	data = ""
	if os.path.exists(file_):
		readed = pd.read_csv(file_, usecols=[9,], names=['montant'] , header=None, encoding='cp850')
		readed2 = readed.sum().to_dict()
		details = {
			'filename': filename,
			'lignes': readed.size,
			'montant' : readed2['montant']
		}
		data = pd.read_csv(file_, header=None, encoding='cp850')
		print(data)
		i = 0
		for index, row in data.iterrows():
			facture = Facture.objects.create(
				agence 			=row[0],
				centre 			=row[1],
#				user_ref		=row[2],
				ref				=row[2],
				panneau 		=row[3],
				annee_conso		=row[4],
				periode_conso 	=row[5],
				annee_factu		=row[6],
				periode_factu 	=row[7],
				montant_conso 	=row[8],
				montant_ht 		=row[9],
				nufmmr 			=row[10],
				montant_surtaxe =row[11],
				contribution	=row[12],
				montant_ttc 	=row[13],
				net_a_payer		=row[14],
				piece_conso		=row[15],
				taux_tva		=row[16],
				montant_tva 	=row[17],
				conso_facture	=row[18],
				jours_conso		=row[19],
				old_index 		=row[20],
				new_index 		=row[21],
				date_releve 	=row[22],
				tarif 			=row[23],
				date_limite 	=row[24],
				nom_abonne 		="nom "+str(i),
				adresse 		=row[26],
				montant_lht 	=row[27],
				montant_al 		=row[28],
			)
			i=i+1
			print(i)

		# Enregister dans la base de données  --------------------------------

		# compresser en xz -----------------------------------------
		# dest_file = 'archives/factures/{}.xz'.format(filename) #dossier et nom de destination
		# dest_file = os.path.join(FILE_ROOT, dest_file)
		# with open(file_, 'rb') as f, open(dest_file, 'wb') as out:
		#     out.write(xz.compress(bytes(f.read())))


		# if os.path.exists(dest_file):
		# 	file_ = os.path.join(FILE_ROOT, 'toto.txt')
		# 	os.remove(file_)

		fichier = Fichier.objects.create(nom=details['filename'], lignes=details['lignes'], montant=details['montant'])

		context={
			'details' : details,
			'data': 	data,
		}
	else:
		print('Le fichier', filename, end=' n\'existe pas.\n ')

	context.update({'fichier_list' : Fichier.objects.all()})
	print("Temps d execution : %s secondes ---" % (time.time() - start_time))
	#return HttpResponse(details['lignes'])
	return HttpResponse('fichier '+filename+' chargé ( '+str(details['lignes'])+' lignes )')

def reglements(request):
	# la date d'hier
	#date = (datetime.date.today()-datetime.timedelta(1)).strftime("%d-%m-%y")
	date = datetime.date.today().strftime("%d-%m-%y")
	factures = Facture.objects.filter(status='p')
	#print(factures)
	filename = 'reglements_{}.csv'.format(date)
	file_ = os.path.join(FILE_ROOT, filename)

	with open(file_, 'w', newline='', encoding='cp850') as f:
		writer = csv.writer(f)
		writer.writerows(factures)

	return HttpResponse('fichier '+filename+' généré')


@login_required()
def test(request):
	data = (datetime.date.today()-datetime.timedelta(1)).strftime("%d-%m-%y")
	return HttpResponse(data)
