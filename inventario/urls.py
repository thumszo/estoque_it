from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('item/novo/', views.cadastrar_item, name='cadastrar_item'),
    path('item/<int:pk>/editar/', views.editar_item, name='editar_item'),
    path('item/<int:pk>/remover/', views.remover_item, name='remover_item'),
    path('item/movimentar/', views.movimentar_item, name='movimentar_item'),
    path('historico/', views.historico, name='historico'),
    path('exportar/csv/', views.exportar_csv, name='exportar_csv'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
]

