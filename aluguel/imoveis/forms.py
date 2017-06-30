from django import forms

from aluguel.imoveis.models import Imovel


class ImovelForm(forms.ModelForm):

    class Meta:
        model = Imovel
        exclude = ('disponivel', )
