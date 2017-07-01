from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Field
from django import forms

from imoveis.models import Imovel


class ImovelFormHelper(FormHelper):
    html5_required = True
    error_text_inline = True
    form_class = 'post-form'
    layout = Layout(
        'descricao',
        'foto',
        Div(
            Div(
                Div(
                    'endereco',
                    css_class='col-sm-9 post-form-field'
                ),
                Div(
                    'cep',
                    css_class='col-sm-3 post-form-field'
                ),
            ),
            css_class="row",
        ),
        Div(
            Div(
                Div(
                    'uf',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'cidade',
                    css_class='col-sm-3 post-form-field'
                ),
            ),
            css_class="row",
        ),
        Div(
            Div(
                Div(
                    'quartos',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'suites',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'area',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'vagas',
                    css_class='col-sm-3 post-form-field'
                ),
            ),
            css_class="row",
        ),
        Div(
            Div(
                Div(
                    'aluguel',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'condominio',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'iptu',
                    css_class='col-sm-3 post-form-field'
                ),
            ),
            css_class="row",
        ),
        Div(
            Div(
                Div(
                    'telefone',
                    css_class='col-sm-3 post-form-field'
                ),
                Div(
                    'email',
                    css_class='col-sm-9 post-form-field'
                ),
            ),
            css_class="row",
        ),
        FormActions(
            Submit('submit', 'Salvar', css_class='save btn btn-success')
        ),
    )


class ImovelForm(forms.ModelForm):

    class Meta:
        model = Imovel
        exclude = ('disponivel', )

    def __init__(self, *args, **kwargs):
        self.helper = ImovelFormHelper()
        super(ImovelForm, self).__init__(*args, **kwargs)
