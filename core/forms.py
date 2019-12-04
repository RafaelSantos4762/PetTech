from django import forms
from django.core.mail import EmailMessage

from .models import Cliente, Fornecedor, Produto,Pedido


class ClienteForm(forms.Form):

    tipo_pessoa = forms.CharField(required=True)
    nome = forms.CharField(required=True)
    sexo = forms.CharField(required=True)
    cpf_cnpj = forms.CharField(required=True)
    rg = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    estado_civil = forms.CharField(required=True)
    data_nasc = forms.DateField()
    cep = forms.CharField(required=True)
    endereco = forms.CharField(required=True)
    complemento = forms.CharField(required=False)
    numero = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    bairro = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    tipo_tel = forms.CharField(required=True)
    tel = forms.CharField(required=True)


class FornecedorForm(forms.Form):
    tipo_pessoa = forms.CharField(required=True)
    data_cadastro = forms.DateField(required=True)
    nome_fantasia = forms.CharField(required=True)
    razao_social = forms.CharField(required=True)
    cpf_cnpj = forms.CharField(required=True, min_length=11, max_length=14)
    rg_ie = forms.CharField(required=True, min_length=9, max_length=9 )
    cep = forms.CharField(required=True,min_length=8, max_length=8)
    endereco = forms.CharField(required=True)
    numero = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    bairro = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    fax = forms.CharField(required=False)
    tel = forms.CharField(required=True, min_length=10, max_length=11)
    email = forms.EmailField(required=True)


class ProdutoForm(forms.Form):
    # id_produto = forms.IntegerField(required=True)
    cod_bar = forms.IntegerField(required=False,min_value=1, max_value=9999999999999)
    data_cadastro = forms.DateField(required=True)
    descricao = forms.CharField(required=True)
    marca = forms.CharField(required=True)


class PedidoForm(forms.Form):
    cliente = forms.IntegerField()
    pagamento = forms.CharField(max_length=20,required=True)
    vendedor  = forms.CharField(max_length=150,required=True)
    observacao = forms.CharField(max_length=200,required=False) 
    tipo    = forms.CharField(required=True) 

class AgendamentoForm(forms.Form):
    dono = forms.CharField(required=True)
    pet = forms.CharField(required=True)
    data = forms.DateField(required=True)
    hora = forms.TimeField(required=True)
    servico = forms.CharField(required=True)