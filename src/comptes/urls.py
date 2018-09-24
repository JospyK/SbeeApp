from django.conf.urls import url

from factures.views import UserFactureHistoryView
from .views         import ( UserDetailView, UsersDetailView, UserListView, UserEmailActivateView, UserDetailUpdateView, disable_enable_user )

app_name = 'comptes'
urlpatterns = [
    url(r'^$',                          UserDetailView.as_view(),           name='user_detail'),
    url(r'^details/(?P<pk>[\w.@+-]+)/$',UsersDetailView.as_view(), 			name="show" ),
    url(r'^list/$',                  	UserListView.as_view(),				name='user_list'),
    url(r'^details/$',                  UserDetailUpdateView.as_view(),     name='user-update'),
    url(r'history/factures/$',          UserFactureHistoryView.as_view(),   name='user-facture-history'),
    url(r'^email/resend-activation/$',  UserEmailActivateView.as_view(),  	name='resend-activation'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', UserEmailActivateView.as_view(),  name='email-activate'),
    url(r'^deu/(?P<pk>[\w.@+-]+)/$',			disable_enable_user,   					name='disable_enable' ),
]

# compte/email/confirm/asdfads/ -> activation view