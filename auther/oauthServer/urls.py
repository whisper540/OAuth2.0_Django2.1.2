from django.urls import path
from oauthServer import views

urlpatterns = [
    path('', views.server, name='default'),
    path('server', views.server, name='server'),
    path('authorize', views.authorize, name='authorize'),
    path('do_login', views.do_login, name='do_login'),
]
