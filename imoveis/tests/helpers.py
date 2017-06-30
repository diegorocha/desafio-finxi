from base64 import b64decode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


def get_sample_form_data(complete=True):
    test_image = '''
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVQYV2P4DwABAQEAWk1v8QAAAABJRU5ErkJggg==
'''.strip()
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
        data['foto'] = InMemoryUploadedFile(BytesIO(b64decode(test_image)),
                                            field_name='tempfile',
                                            name='tempfile.png',
                                            content_type='image/png',
                                            size=len(test_image),
                                            charset='utf-8',
                                            )
    return data
