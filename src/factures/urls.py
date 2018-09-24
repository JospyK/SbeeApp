from django.conf.urls import url
from .views import FactureListView, FactureDetailView

app_name = 'factures'
urlpatterns = [
    url(r'^$',             FactureListView.as_view(), 	name="index" ),
    url(r'^(?P<pk>\d+)/$', FactureDetailView.as_view(), name="show" ),
]