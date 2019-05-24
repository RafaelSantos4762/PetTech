"""PetTech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('contato/',views.contato,name='contato'),
    path('login/',views.log_in,name='login'),
    path('register/',views.register,name='register'),
    path('registerprodutos/',views.produtos,name='registerprodutos'),
    path('produtos/',views.list_produtos,name='produtos'),
    path('registerclientes/',views.clientes,name='registerclientes'),
    path('clientes/',views.list_clientes,name='clientes'),
    path('pedidos/',views.pedidos,name='pedidos'),
    path('fornecedores/',views.list_fornecedores,name='fornecedores'),
    path('registerfornecedores/',views.fornecedores,name='registerfornecedores'),
    path('agendamentos/',views.agendamentos,name='agendamentos'),
    path('cliente/details/<str:uuid>/', views.client_details, name='detailsclientes'),
    path('fornecedor/details/<str:uuid>/', views.forn_details, name='detailsfornecedores'),
    path('produto/details/<str:uuid>/', views.prod_details, name='detailsprodutos'),

]
