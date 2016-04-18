# coding: utf-8
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    'imoveis.views',
    url(r'^$', 'home', name='home'),
    url(r'^imovel/([0-9]+)/$', views.imovel_detalhe, name='detalhe'),
    url(r'^imovel/([0-9]+)/editar$', views.imovel_editar, name='editar'),
    url(r'^imovel/novo/$', views.imovel_novo, name='novo'),
)