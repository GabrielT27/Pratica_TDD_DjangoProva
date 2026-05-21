from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('linkpedia_app.urls')),  # Conecta as rotas do CRUD
]