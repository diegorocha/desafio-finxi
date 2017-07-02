from random import randrange

from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy

from imoveis.models import Imovel
from imoveis.tests.helpers import get_sample_form_data


class InvalidObjectMixin(object):
    def test_invalido(self):
        Imovel.objects.all().delete()
        self.resp = self.client.get(self.url)
        self.assertEquals(404, self.resp.status_code)


class HomeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('imoveis:home')

    def test_get(self):
        self.resp = self.client.get(self.url)
        self.assertEqual(200, self.resp.status_code)

    def test_home_vazia(self):
        Imovel.objects.all().delete()
        self.resp = self.client.get(self.url)
        self.assertEquals(self.resp.context_data['view'].imoveis().count(), 0)
        self.assertIn('Nenhum imóvel disponível.', self.resp.content.decode('utf-8'))

    def test_home_apenas_disponiveis(self):
        qtd = randrange(1, 10)
        mommy.make(Imovel, _quantity=qtd)
        qtd_disponiveis = Imovel.get_disponiveis().count()
        self.resp = self.client.get(self.url)
        self.assertEquals(self.resp.context_data['view'].imoveis().count(), qtd_disponiveis)
        qtd_div = self.resp.content.decode('utf-8').count('<div class="row imovel">')
        self.assertEquals(qtd_div, qtd_disponiveis)


class DetalheViewTest(InvalidObjectMixin, TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        self.url = reverse('imoveis:detalhe', args=[self.imovel.pk])

    def test_get(self):
        self.resp = self.client.get(self.url)
        self.assertEqual(200, self.resp.status_code)
        self.assertEquals(self.imovel, self.resp.context_data['imovel'])

    def test_anuncio_removido(self):
        self.imovel.remover_anuncio()
        self.resp = self.client.get(self.url)
        self.assertEqual(200, self.resp.status_code)
        self.assertIn('Esse esse imóvel não está mais disponível', self.resp.content.decode('utf-8'))


class EditarViewTest(InvalidObjectMixin, TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        self.url = reverse('imoveis:editar', args=[self.imovel.pk])

    def test_get(self):
        self.resp = self.client.get(self.url)
        self.assertEqual(200, self.resp.status_code)
        self.assertEquals(self.imovel, self.resp.context_data['imovel'])

    def test_invalido(self):
        Imovel.objects.all().delete()
        self.resp = self.client.get(self.url)
        self.assertEqual(404, self.resp.status_code)

    def test_post_com_erro(self):
        # Sem nenhum dado
        resp = self.client.post(self.url)
        # Em caso de sucesso erro retorna a página com erros
        self.assertEqual(200, resp.status_code)
        self.assertGreater(len(resp.context_data['form'].errors), 0)

    def test_post(self):
        new_data = get_sample_form_data()
        resp = self.client.post(self.url, new_data)
        self.imovel.refresh_from_db()
        # Em caso de sucesso redireciona para detalhe
        self.assertRedirects(resp, reverse('imoveis:detalhe', args=[self.imovel.pk]))
        self.assertEquals(new_data['endereco'], self.imovel.endereco)


class RemoverViewTest(TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        self.url = reverse('imoveis:remover', args=[self.imovel.pk])

    def test_get(self):
        resp = self.client.get(self.url)
        # GET não permitido
        self.assertEquals(405, resp.status_code)

    def test_post(self):
        resp = self.client.post(self.url, follow=True)
        self.imovel.refresh_from_db()
        # Em caso de sucesso redireciona para home
        self.assertRedirects(resp, reverse('imoveis:home'))
        self.assertFalse(self.imovel.disponivel)

    def test_invalido(self):
        Imovel.objects.all().delete()
        self.resp = self.client.post(self.url)
        self.assertEquals(404, self.resp.status_code)


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
        self.assertGreater(len(resp.context_data['form'].errors), 0)

    def test_post(self):
        qtd_antes = Imovel.objects.count()
        resp = self.client.post(self.url, get_sample_form_data())
        qtd_depois = Imovel.objects.count()
        # Em caso de sucesso redireciona para home
        self.assertRedirects(resp, reverse('imoveis:home'))
        self.assertEquals(qtd_antes + 1, qtd_depois)


class BuscaViewTest(TestCase):
    def setUp(self):
        mommy.make(Imovel, endereco='Rua Cândido Benício, 1300', cidade='Rio de Janeiro', latitude=None, longitude=None)
        self.url = reverse('imoveis:busca')

    def test_get(self):
        # É esperado que uma busca vazia seja redirecionada para home
        self.resp = self.client.get(self.url)
        self.assertRedirects(self.resp, reverse('imoveis:home'))

    def test_busca_endereco_invalido(self):
        resp = self.client.get(reverse('imoveis:busca', args=[' ']))
        self.assertEqual(200, resp.status_code)
        self.assertIsNone(resp.context_data['view'].result())

    def test_busca_endereco_ok(self):
        resp = self.client.get(reverse('imoveis:busca', args=['Rua Baronesa, 175']))
        self.assertEqual(200, resp.status_code)
        self.assertEquals(1, len(resp.context_data['view'].result()['imoveis']))

    def test_busca_endereco_nenhum_resultado(self):
        resp = self.client.get(reverse('imoveis:busca', args=['Rua Vieira Souto, Rio de Janeiro']))
        self.assertEqual(200, resp.status_code)
        self.assertEquals(0, len(resp.context_data['view'].result()['imoveis']))

    def test_busca_endereco_sem_dados(self):
        Imovel.objects.all().delete()
        resp = self.client.get(reverse('imoveis:busca', args=['Rua Baronesa, 175']))
        self.assertEqual(200, resp.status_code)
        self.assertEquals(0, len(resp.context_data['view'].result()['imoveis']))
