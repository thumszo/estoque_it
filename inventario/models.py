from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):  # Categoria serve para agrupar os itens (ex: Teclado, Mouse, Toner)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome  # Mostra o nome da categoria no admin e nos templates

class Item(models.Model):   # Representa um item do estoque
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Cada item pertence a uma categoria
    quantidade = models.PositiveIntegerField(default=0)  # Quantidade atual no estoque
    estoque_minimo = models.PositiveIntegerField(default=1)  # Quantidade mínima desejada (para alertas)
    descricao = models.TextField(blank=True)  # Campo opcional para observações

    class Meta:
        unique_together = ('nome', 'categoria')  # Impede que exista mais de um item com o mesmo nome e categoria

    def __str__(self):
        return self.nome  # Nome exibido no admin e nas interfaces

class Movimento(models.Model):  # Representa uma movimentação de entrada ou saída de um item do estoque
    TIPO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Qual item foi movimentado
    tipo = models.CharField(max_length=7, choices=TIPO)   # Tipo: entrada ou saída
    quantidade = models.PositiveIntegerField()   # Quantidade movimentada
    data = models.DateTimeField(auto_now_add=True)   # Data/hora da movimentação
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Quem fez a movimentação

    def __str__(self):
        return f"{self.tipo} - {self.item.nome} - {self.quantidade}"  # Exibição no admin
