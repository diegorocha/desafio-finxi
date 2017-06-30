# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View

from .helpers import get_coordenates
from .models import Imovel
from .forms import ImovelForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def imoveis(self):
        return Imovel.get_disponiveis()


class ImovelDetailView(DetailView):
    template_name = 'detalhe.html'
    queryset = Imovel.objects.all()
    pk_field = 'pk'
    pk_url_kwarg = 'imovel_id'
    context_object_name = 'imovel'


class NovoImovelView(CreateView):
    template_name = 'editar.html'
    form_class = ImovelForm

    def get_success_url(self):
        return reverse('imoveis:home')


class EditarImovelView(UpdateView):
    template_name = 'editar.html'
    form_class = ImovelForm
    queryset = Imovel.objects.all()
    pk_field = 'pk'
    pk_url_kwarg = 'imovel_id'


class RemoverAnuncioView(View):

    def post(self, request, *args, **kwargs):
        imovel = get_object_or_404(Imovel, pk=kwargs.get('imovel_id'))
        imovel.remover_anuncio()
        return redirect('imoveis:home')


class BuscaView(TemplateView):
    template_name = 'busca.html'
    endereco = None
    coordenadas = None

    def dispatch(self, request, *args, **kwargs):
        self.endereco = self.kwargs.get('endereco') or self.request.GET.get('q')
        if not self.endereco:
            # Sem endereço: Atualiza uma pesquisa sem conteúdo pra home
            return redirect('imoveis:home')
        return super(BuscaView, self).dispatch(request, *args, **kwargs)

    def result(self):
        self.coordenadas = get_coordenates(self.endereco)
        if self.coordenadas:
            dados = {'endereco': self.endereco}
            dados['imoveis'] = Imovel.get_proximos_a(latitude=self.coordenadas[0],
                                                     longitude=self.coordenadas[1])
            dados['endereco_formatado'] = self.coordenadas[2]
            return dados
