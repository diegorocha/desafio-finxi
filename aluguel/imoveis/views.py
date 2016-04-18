# coding: utf-8
from django.shortcuts import render
from .forms import ImovelForm



def home(request):
    return render(request, 'home.html')

def imovel_novo(request):
    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = ImovelForm()
    return render(request, 'imovel_novo.html', {'form': form})