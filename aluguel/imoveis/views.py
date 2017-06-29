# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import DetailView
from django.views.generic import TemplateView

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


def imovel_novo(request):
    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.save()
            return redirect('imoveis:home')
    else:
        form = ImovelForm()
    return render(request, 'editar.html', {'form': form})


def imovel_editar(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    if request.method == "POST":
        form = ImovelForm(request.POST, instance=imovel)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.save()
            return redirect('imoveis:detalhe', imovel.pk)
    else:
        form = ImovelForm(instance=imovel)
    return render(request, 'editar.html', {'form': form})


@requires_csrf_token
def imovel_remover_anuncio(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    if request.method == "POST":
        imovel.remover_anuncio()
        return redirect('imoveis:home')
    else:
        return redirect('imoveis:editar', imovel_id)


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
