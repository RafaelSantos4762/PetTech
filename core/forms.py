from django import forms
from django.core.mail import EmailMessage


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
    data_cadastro = forms.DateField()
    nome_fantasia = forms.CharField(required=True)
    razao_social = forms.CharField(required=True)
    cpf_cnpj = forms.CharField(required=True)
    rg_ie = forms.CharField(required=True)
    cep = forms.CharField(required=True)
    endereco = forms.CharField(required=True)
    numero = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    bairro = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    fax = forms.CharField(required=False)
    tel = forms.CharField(required=True)
    email = forms.EmailField(required=True)


class ProdutoForm(forms.Form):
    # id_produto = forms.IntegerField(required=True)
    cod_bar = forms.IntegerField(required=True,min_value=0, max_value=9999999999999)
    data_cadastro = forms.DateField(required=True)
    descricao = forms.CharField(required=True)
    marca = forms.CharField(required=True)
    custo = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=True)
    venda = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=True)
    estoque = forms.IntegerField(label=0)
