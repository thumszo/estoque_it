from django.shortcuts import render, redirect, get_object_or_404  # Importa funções utilitárias do Django para redirecionar, renderizar e buscar objetos no banco
from .models import Item
from .forms import ItemForm
from .models import Movimento   # Importa os modelos usados no sistema: Item, Categoria, Movimento
from .forms import ItemForm, MovimentoForm   # Importa os formulários personalizados do app
from django.contrib.auth.forms import UserCreationForm   # Importa o formulário padrão de criação de usuários do Django
from django.contrib.auth import login  # Para logar o usuário após o cadastro
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test  # Decoradores para exigir que o usuário esteja logado ou faça parte de um grupo
import csv  # Bibliotecas para exportação
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@login_required
def listar_itens(request):
    itens = Item.objects.all()
    return render(request, 'inventario/listar_itens.html', {'itens': itens})

def is_admin(user):  # View auxiliar para verificar se o usuário está no grupo "admin"
    return user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin)
def cadastrar_item(request):  # Tela de cadastro de novo item (apenas para admin)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'inventario/form_item.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def editar_item(request, pk):  # Tela para editar um item já existente (admin)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventario/form_item.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def remover_item(request, pk):  # Tela para confirmar e remover item (admin)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard')
    return render(request, 'inventario/confirmar_remocao.html', {'item': item})

@login_required
def movimentar_item(request):  # Tela para registrar entrada ou saída de estoque
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)  
            movimento.usuario = request.user  # Salva o usuário que fez a movimentação
            item = movimento.item
            if movimento.tipo == 'entrada':  # Atualiza o estoque com base no tipo de movimentação
                item.quantidade += movimento.quantidade
            elif movimento.tipo == 'saida':
                item.quantidade -= movimento.quantidade
            item.save()
            movimento.save()
            return redirect('dashboard')
    else:
        form = MovimentoForm()
    return render(request, 'inventario/form_movimentacao.html', {'form': form})

@login_required
def historico(request):  # Exibe o histórico de movimentações (entradas e saídas)
    historico = Movimento.objects.all().order_by('-data')
    return render(request, 'inventario/historico.html', {'historico': historico})

@login_required
def dashboard(request):  # Exibe todos os itens na tela principal (dashboard)
    itens = Item.objects.all()
    is_admin = request.user.groups.filter(name='admin').exists()
    return render(request, 'inventario/dashboard.html', {
        'itens': itens,
        'is_admin': is_admin
    })

def register(request):  # Tela de cadastro de novo usuário
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário automaticamente
            return render(request, 'inventario/register_success.html')  
    else:
        form = UserCreationForm()
    return render(request, 'inventario/register.html', {'form': form})

def error_403(request, exception=None):  # Tela personalizada para erro de permissão negada (403)
    return render(request, '403.html', {
        'exception': exception
    }, status=403)

@login_required
def exportar_csv(request):  # Exporta todos os itens do estoque para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="estoque.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Categoria', 'Quantidade', 'Estoque Mínimo', 'Descrição'])

    for item in Item.objects.all():
        writer.writerow([
            item.nome,
            item.categoria.nome,
            item.quantidade,
            item.estoque_minimo,
            item.descricao,
        ])

    return response

@login_required
def exportar_pdf(request):  # Exporta todos os itens do estoque para um PDF formatado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estoque.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Relatório de Estoque de Insumos de TI")
    y -= 40

    p.setFont("Helvetica", 10)
    for item in Item.objects.all():
        texto = f"{item.nome} ({item.categoria}) - {item.quantidade} unidades [mín: {item.estoque_minimo}]"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response