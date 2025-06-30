from django.contrib import admin
from .models import Categoria, Item, Movimento

admin.site.site_header = "Administração do Sistema"
admin.site.site_title = "Administração do Sistema"
admin.site.index_title = "Painel de Controle"

admin.site.register(Categoria)
admin.site.register(Item)
admin.site.register(Movimento)
