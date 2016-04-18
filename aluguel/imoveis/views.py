# coding: utf-8
from django.shortcuts import render, get_object_or_404
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
    return render(request, 'novo.html', {'form': form})