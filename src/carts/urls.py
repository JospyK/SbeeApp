from django.conf.urls import url
from .views import home, update, checkout

app_name = 'carts'
urlpatterns = [
    url(r'^$', home, name="index"),
    url(r'^update/$', update, name="update" ),
    url(r'^checkout/$', checkout, name="checkout" ),
]
