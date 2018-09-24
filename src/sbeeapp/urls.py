"""sbeeapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView
from .views import home_page, dash_page, contact_page
from comptes.views import LoginView, RegisterView

urlpatterns = [
    url(r'^$', home_page),
    url(r'^dashboard/$',    dash_page,      name='dash'),
    url(r'^contact/$',      contact_page,   name='contact'),
    url(r'^login/$',        LoginView.as_view(), name='login'),
    url(r'^logout/$',       LogoutView.as_view(),   name='logout'),
    url(r'^register/$',     RegisterView.as_view(), name='register'),
    
    url(r'^admin/',     admin.site.urls),
    url(r'^factures/',  include('factures.urls',    namespace='factures')),
    url(r'^fichiers/',  include('fichiers.urls',    namespace='fichiers')),
    url(r'^carts/',     include('carts.urls',       namespace='carts')),
    url(r'^compte/',    include('comptes.urls',     namespace='compte')),
    url(r'^comptes/',   include('comptes.passwords.urls', namespace='comptes')),
    url(r'^comptes/',   RedirectView.as_view(url='/compte')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns+static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
