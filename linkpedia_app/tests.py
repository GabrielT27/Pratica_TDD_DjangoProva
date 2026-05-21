from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LinkModel

class LinkpediaTests(TestCase):

    def setUp(self):
        # Usuário válido seguindo a regra da Sprint 1
        self.user_valido = User.objects.create_user(
            username='aluno',
            email='aluno@cps.sp.gov.br',
            password='fatec'
        )
        # Link inicial para testes de edição/remoção
        self.link = LinkModel.objects.create(
            user=self.user_valido,
            titulo='GitHub do Professor',
            url='https://github.com/orlandosaraivajr'
        )

    def test_usuario_nao_logado_eh_bloqueado(self):
        """Sprint 2: Garante que rotas do CRUD exigem login (Redirecionamento 302)"""
        rotas = [
            reverse('listar_links'),
            reverse('cadastrar_link'),
            reverse('atualizar_link', args=[self.link.pk]),
            reverse('remover_link', args=[self.link.pk])
        ]
        for rota in rotas:
            response = self.client.get(rota)
            self.assertEqual(response.status_code, 302)

    def test_listar_links_usuario_logado(self):
        """Sprint 2: Usuário logado consegue ver seus links"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(reverse('listar_links'))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_link_valido(self):
        """Sprint 2: Cadastro de link com sucesso via POST"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.post(reverse('cadastrar_link'), {
            'titulo': 'Site CPS',
            'url': 'https://www.cps.sp.gov.br'
        })
        self.assertRedirects(response, reverse('listar_links'))
        self.assertTrue(LinkModel.objects.filter(titulo='Site CPS').exists())

    def test_cadastrar_link_get(self):
        """Testa o carregamento da página de cadastro (GET)"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(reverse('cadastrar_link'))
        self.assertEqual(response.status_code, 200)

    def test_atualizar_link_valido(self):
        """Sprint 2: Atualização de link existente"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.post(reverse('atualizar_link', args=[self.link.pk]), {
            'titulo': 'GitHub Atualizado',
            'url': 'https://github.com'
        })
        self.assertRedirects(response, reverse('listar_links'))
        self.link.refresh_from_db()
        self.assertEqual(self.link.titulo, 'GitHub Atualizado')

    def test_atualizar_link_get(self):
        """Testa o carregamento da página de edição (GET)"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(reverse('atualizar_link', args=[self.link.pk]))
        self.assertEqual(response.status_code, 200)

    def test_remover_link_post(self):
        """Sprint 2: Remoção de link existente via POST"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.post(reverse('remover_link', args=[self.link.pk]))
        self.assertRedirects(response, reverse('listar_links'))
        self.assertFalse(LinkModel.objects.filter(pk=self.link.pk).exists())

    def test_remover_link_get(self):
        """Testa a página de confirmação de exclusão (GET)"""
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(reverse('remover_link', args=[self.link.pk]))
        self.assertEqual(response.status_code, 200)

    def test_modelo_string_representation(self):
        """Testa o método __str__ do modelo para cobrir 100% do models.py"""
        self.assertEqual(str(self.link), 'GitHub do Professor')