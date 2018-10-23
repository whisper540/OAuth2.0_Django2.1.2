from django.urls import path
from oauthClient import views

urlpatterns = [
    path('', views.client, name='default'),
    path('client', views.client, name='client'),
    path('authorize', views.authorize, name='authorize'),
    path('test', views.test, name='test'),
]
