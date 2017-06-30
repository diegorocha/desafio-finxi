# coding: utf-8
from django.conf.urls import patterns, url

from aluguel.imoveis.views import HomeView, ImovelDetailView, BuscaView, NovoImovelView, EditarImovelView, RemoverAnuncioView

urlpatterns = patterns(
    'imoveis.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^imovel/(?P<imovel_id>[0-9]+)/$', ImovelDetailView.as_view(), name='detalhe'),
    url(r'^imovel/(?P<imovel_id>[0-9]+)/editar$', EditarImovelView.as_view(), name='editar'),
    url(r'^imovel/(?P<imovel_id>[0-9]+)/remover$', RemoverAnuncioView.as_view(), name='remover'),
    url(r'^imovel/novo/$', NovoImovelView.as_view(), name='novo'),
    url(r'^busca/$', BuscaView.as_view(), name='busca'),
    url(r'^busca/(?P<endereco>.+)/$', BuscaView.as_view(), name='busca'),
)
