from django.shortcuts import render, redirect, get_object_or_404  # <-- Corrigido aqui
from django.contrib.auth.decorators import login_required
from .models import LinkModel
from .forms import LinkForm

@login_required
def listar_links(request):
    links = LinkModel.objects.filter(user=request.user)
    return render(request, 'links/listar.html', {'links': links})

@login_required
def cadastrar_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('listar_links')
    else:
        form = LinkForm()
    return render(request, 'links/form.html', {'form': form, 'acao': 'Cadastrar'})

@login_required
def atualizar_link(request, pk):
    link = get_object_or_404(LinkModel, pk=pk, user=request.user)  # <-- Corrigido aqui
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('listar_links')
    else:
        form = LinkForm(instance=link)
    return render(request, 'links/form.html', {'form': form, 'acao': 'Atualizar'})

@login_required
def remover_link(request, pk):
    link = get_object_or_404(LinkModel, pk=pk, user=request.user)  # <-- Corrigido aqui
    if request.method == 'POST':
        link.delete()
        return redirect('listar_links')
    return render(request, 'links/confirmar_exclusao.html', {'link': link})