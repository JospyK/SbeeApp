# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-13 21:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agence', models.IntegerField(help_text='AGENCE PAYEUR', verbose_name='AGENCE PAYEUR')),
                ('centre', models.IntegerField(help_text='CENTRE PAYEUR', verbose_name='CENTRE PAYEUR')),
                ('panneau', models.CharField(help_text='PANNEAU', max_length=8, verbose_name='PANNEAU')),
                ('ref', models.CharField(help_text='REFERENCE ABONNE', max_length=30, verbose_name='REFERENCE ABONNE')),
                ('annee_conso', models.IntegerField(help_text='ANNEE DE CONSOMMATION', verbose_name='ANNEE DE CONSOMMATION')),
                ('periode_conso', models.IntegerField(help_text='PERIODE DE CONSOMMATION', verbose_name='PERIODE DE CONSOMMATION')),
                ('annee_factu', models.IntegerField(help_text='ANNEE DE FACTURATION', verbose_name='ANNEE DE FACTURATION')),
                ('periode_factu', models.IntegerField(help_text='PERIODE DE FACTURATION', verbose_name='PERIODE DE FACTURATION')),
                ('montant_conso', models.IntegerField(help_text='MONTANT CONSOMMATION', verbose_name='MONTANT CONSOMMATION')),
                ('montant_ht', models.IntegerField(help_text='MONTANT HORS TAXE', verbose_name='MONTANT HORS TAXE')),
                ('nufmmr', models.CharField(help_text='digits(nufmmr)', max_length=12, verbose_name='digits(nufmmr)')),
                ('montant_surtaxe', models.IntegerField(help_text='MONTANT SURTAXE', verbose_name='MONTANT SURTAXE')),
                ('contribution', models.IntegerField(help_text='CONTRIBUTION ELEC/RURALE', verbose_name='CONTRIBUTION ELEC/RURALE')),
                ('montant_ttc', models.IntegerField(help_text='MONTANT TTC', verbose_name='MONTANT TTC')),
                ('net_a_payer', models.IntegerField(help_text='NET A PAYER', verbose_name='NET A PAYER')),
                ('piece_conso', models.CharField(help_text='TYPE PIECE CONSOM.', max_length=3, verbose_name='TYPE PIECE CONSOM.')),
                ('taux_tva', models.IntegerField(help_text='TAUX TVA', verbose_name='TAUX TVA')),
                ('montant_tva', models.IntegerField(help_text='MONTANT TVA', verbose_name='MONTANT TVA')),
                ('conso_facture', models.IntegerField(help_text='Conso facturée', verbose_name='Conso facturée')),
                ('jours_conso', models.IntegerField(help_text='NOMBRE JOURS CONSO', verbose_name='NOMBRE JOURS CONSO')),
                ('old_index', models.IntegerField(help_text='ANCIEN INDEX', verbose_name='ANCIEN INDEX')),
                ('new_index', models.IntegerField(help_text='NOUVEL INDEX', verbose_name='NOUVEL INDEX')),
                ('date_releve', models.IntegerField(help_text='DATE RELEVE', verbose_name='DATE RELEVE')),
                ('tarif', models.CharField(help_text='TARIF', max_length=4, verbose_name='TARIF')),
                ('date_limite', models.IntegerField(help_text='DATE LIMITE PAIEMENT', verbose_name='DATE LIMITE PAIEMENT')),
                ('nom_abonne', models.CharField(help_text='NOM DU PAYEUR', max_length=40, verbose_name='NOM DU PAYEUR')),
                ('adresse', models.CharField(help_text='ADRESSE 1', max_length=40, verbose_name='ADRESSE 1')),
                ('montant_lht', models.IntegerField(help_text='MONTANT LOCATION HT', verbose_name='MONTANT LOCATION HT')),
                ('montant_al', models.IntegerField(help_text='MONTANT AUTRES LOCATIONS', verbose_name='MONTANT AUTRES LOCATIONS')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('p', 'Paye'), ('i', 'Impaye')], default='i', help_text='Paye ou Impaye', max_length=1)),
                ('user_ref', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Reference Abonne')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='FactureManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
