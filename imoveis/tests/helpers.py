from django.core.files.base import ContentFile
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_sample_foto():
    """ Gera uma imagem de 5x5 na memória e retorna um array de bytes"""
    img = Image.new('RGB', (5, 5))
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    buffer = img_bytes.getvalue()
    return ContentFile(buffer)


def get_sample_form_data(complete=True):
    image_sample = get_sample_foto()
    data = {}
    data['descricao'] = 'Teste'
    data['endereco'] = 'Rua Baronesa, 175'
    data['cep'] = '21321000'
    data['uf'] = 'RJ'
    data['cidade'] = 'Rio de Janeiro'
    data['quartos'] = '3'
    data['suites'] = '2'
    data['area'] = '40'
    data['vagas'] = '1'
    data['aluguel'] = '1000'
    data['condominio'] = '200'
    data['iptu'] = '50'
    data['telefone'] = '123456789'
    data['email'] = 'email@example.com'
    if complete:
        data['foto'] = InMemoryUploadedFile(image_sample,
                                            field_name='foto',
                                            name='tempfile.png',
                                            content_type='image/png',
                                            size=image_sample.size,
                                            charset='utf-8',
                                            )
    return data
