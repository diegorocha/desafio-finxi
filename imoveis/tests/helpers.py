from django.core.files.base import ContentFile
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from model_mommy import mommy

from imoveis.models import Imovel


def get_sample_foto():
    """ Gera uma imagem de 5x5 na memória e retorna um array de bytes"""
    img = Image.new('RGB', (5, 5))
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    buffer = img_bytes.getvalue()
    return ContentFile(buffer)


def get_sample_form_data(with_photo=True):
    image_sample = get_sample_foto()
    # Precisa ser um endereço válido
    mock_imovel = mommy.prepare(Imovel, endereco='Rua Baronesa, 175', cidade='Rio de Janeiro', uf='RJ', _fill_optional=True)
    data = {}
    data['descricao'] = mock_imovel.descricao
    data['endereco'] = mock_imovel.endereco
    data['cep'] = mock_imovel.cep
    data['uf'] = mock_imovel.uf
    data['cidade'] = mock_imovel.cidade
    data['quartos'] = mock_imovel.quartos
    data['suites'] = mock_imovel.suites
    data['area'] = mock_imovel.area
    data['vagas'] = mock_imovel.vagas
    data['aluguel'] = mock_imovel.aluguel
    data['condominio'] = mock_imovel.condominio
    data['iptu'] = mock_imovel.iptu
    data['telefone'] = mock_imovel.telefone
    data['email'] = mock_imovel.email
    if with_photo:
        data['foto'] = InMemoryUploadedFile(image_sample,
                                            field_name='foto',
                                            name='tempfile.png',
                                            content_type='image/png',
                                            size=image_sample.size,
                                            charset='utf-8',
                                            )
    return data
