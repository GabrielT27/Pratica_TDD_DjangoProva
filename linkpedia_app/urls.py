from django.urls import path
from . import views

urlpatterns = [
    path('links/', views.listar_links, name='listar_links'),
    path('links/novo/', views.cadastrar_link, name='cadastrar_link'),
    path('links/editar/<int:pk>/', views.atualizar_link, name='atualizar_link'),
    path('links/deletar/<int:pk>/', views.remover_link, name='remover_link'),
]