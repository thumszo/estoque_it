from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Item(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=1)
    descricao = models.TextField(blank=True)

    class Meta:
        unique_together = ('nome', 'categoria')

    def __str__(self):
        return self.nome

class Movimento(models.Model):
    TIPO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.item.nome} - {self.quantidade}"
