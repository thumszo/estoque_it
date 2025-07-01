from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventario import views as inventario_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventario/logout.html'), name='logout'),
    path('register/', inventario_views.register, name='register'),
]
