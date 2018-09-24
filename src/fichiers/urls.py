from django.conf.urls import url
from .views import FichierListView, FichierDetailView, reglements, loaddt, test

app_name = 'fichiers'
urlpatterns = [
    url(r'^$',				FichierListView.as_view(), 		name="list" ),
    url(r'^reglement/$',	reglements,   					name='reglement' ),
    url(r'^load/$',			loaddt,   						name='load' ),
    url(r'^t/$',			test,   						name='test' ),
    url(r'^(?P<pk>\d+)/$',	FichierDetailView.as_view(),	name="show" ),
]