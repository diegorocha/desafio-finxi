from django.test import TestCase

from imoveis.forms import ImovelForm
from imoveis.tests.helpers import get_sample_form_data


class ImovelFormTest(TestCase):

    def test_form_invalid(self):
        form = ImovelForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_sem_foto_invalido(self):
        form = ImovelForm(get_sample_form_data(with_photo=False))
        self.assertFalse(form.is_valid())
        self.assertIn('foto', form.errors)

    def test_form_valid(self):
        data = get_sample_form_data()
        foto = {'foto': data['foto']}
        form = ImovelForm(data, foto)
        self.assertTrue(form.is_valid())
