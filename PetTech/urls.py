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
from django.urls import path,include
#from core.views import getProdutos
from core import views
from django.conf import settings
#from django.conf.urls.static import static

#from django.conf.urls import url, include
from django.contrib.auth.models import User
#from rest_framework import routers, serializers, viewsets


# Routers provide an easy way of automatically determining the URL conf.
#router = routers.DefaultRouter()
#router.register('getprodutos', getProdutos)

urlpatterns = [
    #path('api/', include(router.urls)),
    path('admin/', admin.site.urls,name="admin"),
    path('register/', views.signup,name="register"),
    path('login/', views.login_user,name="login"),
    path('login/submit', views.submit_login,name="submit"),
    path('logout/', views.logout_user,name="logout"),
    path('', views.index,name="index"),
    path('registerprodutos/',views.produtos,name='registerprodutos'),
    path('produtos/',views.list_produtos,name='produtos'),
    path('registerpedidos/',views.pedidos,name='registerpedidos'),
    path('registerclientes/',views.clientes,name='registerclientes'),
    path('clientes/',views.list_clientes,name='clientes'),
    path('pedidos/',views.list_pedidos,name='pedidos'),
    path('fornecedores/',views.list_fornecedores,name='fornecedores'),
    path('registerfornecedores/',views.fornecedores,name='registerfornecedores'),
    path('createsales/',views.pedidos,name='createsales'),
    path('registeragenda/',views.agendamentos,name='registeragenda'),
    path('agendamentos/',views.list_agendamentos,name='agendamentos'),
    path('servicos/',views.list_servicos,name='listservicos'),
    path('registerservicos/',views.servicos,name='registerservicos'),
    path('clientes/details/<str:id_cliente>/', views.client_details, name='detailsclientes'),
    path('fornecedores/details/<str:id_fornecedor>/', views.forn_details, name='detailsfornecedores'),
    path('produtos/details/<str:id_produto>/', views.prod_details, name='detailsprodutos'),
    path('pedidos/details/<str:id_pedido>/', views.ped_details, name='detailspedidos'),
    path('agendamentos/details/<str:id_servico>/', views.agendamento_details, name='detailsagendamentos'),
]
