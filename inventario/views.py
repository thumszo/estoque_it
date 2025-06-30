from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Categoria
from .forms import ItemForm
from .models import Movimento
from .forms import ItemForm, MovimentoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@login_required
def listar_itens(request):
    itens = Item.objects.all()
    return render(request, 'inventario/listar_itens.html', {'itens': itens})

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin)
def cadastrar_item(request):
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
def editar_item(request, pk):
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
def remover_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard')
    return render(request, 'inventario/confirmar_remocao.html', {'item': item})

@login_required
def movimentar_item(request):
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.usuario = request.user 
            item = movimento.item
            if movimento.tipo == 'entrada':
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
def historico(request):
    historico = Movimento.objects.all().order_by('-data')
    return render(request, 'inventario/historico.html', {'historico': historico})

@login_required
def dashboard(request):
    itens = Item.objects.all()
    is_admin = request.user.groups.filter(name='admin').exists()
    return render(request, 'inventario/dashboard.html', {
        'itens': itens,
        'is_admin': is_admin
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loga automaticamente
            return render(request, 'inventario/register_success.html')  # mostra a nova tela
    else:
        form = UserCreationForm()
    return render(request, 'inventario/register.html', {'form': form})

def error_403(request, exception=None):
    return render(request, '403.html', {
        'exception': exception
    }, status=403)

@login_required
def exportar_csv(request):
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
def exportar_pdf(request):
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