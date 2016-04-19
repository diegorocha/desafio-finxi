# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import requires_csrf_token
from .helpers import get_coordenates
from .models import Imovel
from .forms import ImovelForm


def home(request):
    imoveis = Imovel.get_disponiveis()
    return render(request, 'home.html', {'imoveis': imoveis})


def imovel_detalhe(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    return render(request, 'detalhe.html', {'imovel': imovel})


def imovel_novo(request):
    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = ImovelForm()
    return render(request, 'editar.html', {'form': form})


def imovel_editar(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    if request.method == "POST":
        form = ImovelForm(request.POST, instance=imovel)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('imoveis:detalhe', imovel_id)
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


def busca(request, endereco=None):
    if not endereco:
        endereco = request.GET.get('q', None)
    if endereco:
        coordenadas = get_coordenates(endereco)
        if coordenadas:
            dados = {'endereco': endereco}
            dados['imoveis'] = Imovel.get_proximos_a(latitude=coordenadas[0], 
                                                     longitude=coordenadas[1])
            dados['endereco_formatado'] = coordenadas[2]
            return render(request, 'busca.html', dados)
        else:
            return render(request, 'busca_nao_encontrada.html', {'endereco': endereco})
    else:
        return redirect('imoveis:home')