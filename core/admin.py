from django.contrib import admin
from .models import Cliente
from .models import Produto
# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome','tipo_pessoa','sexo','cpf_cnpj','rg','email','estado']

@admin.register(Produto)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id','cod_bar','data_cadastro','descricao']