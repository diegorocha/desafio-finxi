from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy

from imoveis.models import Imovel
from imoveis.tests.helpers import get_sample_form_data


class HomeViewTest(TestCase):
    def setUp(self):
        url = reverse('imoveis:home')
        self.resp = self.client.get(url)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)


class DetalheViewTest(TestCase):
    def setUp(self):
        imovel = mommy.make(Imovel)
        url = reverse('imoveis:detalhe', args=[imovel.pk])
        self.resp = self.client.get(url)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)


class EditarViewTest(TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        self.url = reverse('imoveis:editar', args=[self.imovel.pk])
        self.resp = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_post_com_erro(self):
        # Sem nenhum dado
        resp = self.client.post(self.url)
        # Em caso de sucesso erro retorna a página com erros
        self.assertEqual(200, resp.status_code)

    def test_post(self):
        resp = self.client.post(self.url, get_sample_form_data())
        # Em caso de sucesso redireciona para detalhe
        self.assertRedirects(resp, reverse('imoveis:detalhe', args=[self.imovel.pk]))


class RemoverViewTest(TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        self.url = reverse('imoveis:remover', args=[self.imovel.pk])

    def test_get(self):
        resp = self.client.get(self.url, follow=True)
        # Se for get redireciona para edição
        self.assertEquals(405, resp.status_code)

    def test_post(self):
        resp = self.client.post(self.url, follow=True)
        # Em caso de sucesso redireciona para home
        self.assertRedirects(resp, reverse('imoveis:home'))


class NovoViewTest(TestCase):
    def setUp(self):
        self.url = reverse('imoveis:novo')

    def test_get(self):
        self.assertEqual(200, self.client.get(self.url).status_code)

    def test_post_com_erro(self):
        # Sem nenhum dado
        resp = self.client.post(self.url)
        # Em caso de sucesso erro retorna a página com erros
        self.assertEqual(200, resp.status_code)

    def test_post(self):
        resp = self.client.post(self.url, get_sample_form_data())
        # Em caso de sucesso redireciona para home
        self.assertRedirects(resp, reverse('imoveis:home'))


class BuscaViewTest(TestCase):
    def setUp(self):
        self.url = reverse('imoveis:busca')
        self.resp = self.client.get(self.url)

    def test_get(self):
        # É esperado que uma busca vazia seja redirecionada para home
        self.assertRedirects(self.resp, reverse('imoveis:home'))

    def test_busca_endereco_invalido(self):
        resp = self.client.get(reverse('imoveis:busca', args=['Rua que não existe']))
        self.assertEqual(200, resp.status_code)

    def test_busca_endereco_ok(self):
        resp = self.client.get(reverse('imoveis:busca', args=['Rua Cândido Benício, 1300, Rio de Janeiro']))
        self.assertEqual(200, resp.status_code)

    def test_busca_endereco_sem_dados(self):
        resp = self.client.get(reverse('imoveis:busca', args=['Rua Vieira Souto, Rio de Janeiro']))
        self.assertEqual(200, resp.status_code)
