# coding: utf-8
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    'imoveis.views',
    url(r'^$', 'home', name='home'),
    url(r'^imovel/novo/$', views.imovel_novo, name='imovel_novo'),
)