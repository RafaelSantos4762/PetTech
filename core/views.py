from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from .forms import ContatoForm, ClienteForm, FornecedorForm, ProdutoForm

from .models import Cliente, Fornecedor, Produto

import uuid

def index(request):
    context = {
     "titulo":"INDEX"
    }
    return render(request,'index.html',context)

def home(request):
    context = {
     "titulo":"HOME"
    }
    return render(request,'home.html',context)

def contato(request):
    context = {}
    if request.POST:
        form = ContatoForm(request.POST)
        if form.is_valid():
            context["mensagem"] = "Formulário enviado com sucesso!"
        else:
            context["mensagem"] = "Formulário Inválido"
    else:
        form = ContatoForm()
        context["form"] = form
    return render(request,'contato.html',context)


def log_in(request):
    """-------------------------------------------------------------------------
    View de login.
    -------------------------------------------------------------------------"""
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # se o formulario for valido
        if form.is_valid():
            # significa que o Django encontrou o usuario no banco de dados
            login(request, form.get_user())
            # redireciona o usuario logado para a pagina inicial(index2)
            return HttpResponseRedirect("/home")
        else:
            return render(request, "login.html", {"form": form})

    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "login.html", {"form": AuthenticationForm()})

def register(request):
    """-------------------------------------------------------------------------
    View de cadastro de usuário.
    -------------------------------------------------------------------------"""
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # cria um novo usuario a partir dos dados enviados
            form.save()
            # redireciona para a tela de login
            return HttpResponseRedirect("/login/")
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "register.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "register.html", {"form": UserCreationForm() })

def produtos(request):
    """-------------------------------------------------------------------------
    View para cadastro de produto.
    -------------------------------------------------------------------------"""
    context = {
     "titulo":"Cadastro de Produto"
    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            id_fornecedor = form.cleaned_data['id_fornecedor']
            cod_bar = form.cleaned_data['cod_bar']
            data_cadastro = form.cleaned_data['data_cadastro']
            descricao = form.cleaned_data['descricao']
            marca = form.cleaned_data['marca']
            custo = form.cleaned_data['custo']
            venda = form.cleaned_data['venda']
            estoque = form.cleaned_data['estoque']
            # gero codigo uuid para a criação da url de detalhes
            cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Produto.objects.create(
                    id_fornecedor = id_fornecedor,
                    cod_bar = cod_bar,
                    data_cadastro = data_cadastro,
                    descricao = descricao,
                    marca = marca,
                    custo = custo,
                    venda = venda,
                    estoque = estoque,
                    uuid = cod
                    )
            # em caso de erro
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context = {
                  "titulo":"Cadastro de Produto",
                  'erro': 'Dados incorretos!'
                }
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/produtos.html", context)
            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/produtos/")
        else:
            # se for um get, renderizo a pagina de cadastro de fornecedor
            return render(request, "./registration/produtos.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/produtos.html", {"form": UserCreationForm()})


def list_produtos(request):
    """-------------------------------------------------------------------------
    View que lista produtos.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    produtos = Produto.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'produtos': produtos
    }

    # Retornamos o template no qual os produtos serão dispostos
    return render(request, "produtos.html", context)

def prod_details(request, uuid):
    """-------------------------------------------------------------------------
    View que mostra detalhes de produto.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o produto
    produto = Produto.objects.get(uuid=uuid)

    # Incluímos no contexto
    context = {
      'produto': produto
    }
    if request.method == 'POST':
        Produto.objects.get(uuid=uuid).delete()
        return HttpResponseRedirect("/produtos/")

    # Retornamos o template no qual o cliente será disposto
    return render(request, "./details/produtos.html", context)



def clientes(request):
    """-------------------------------------------------------------------------
    View para cadastro de cliente.
    -------------------------------------------------------------------------"""
    context = {
     "titulo":"Cadastro de Clientes"
    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            tipo_pessoa = form.cleaned_data['tipo_pessoa']
            nome = form.cleaned_data['nome']
            sexo = form.cleaned_data['sexo']
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            rg = form.cleaned_data['rg']
            email = form.cleaned_data['email']
            estado_civil = form.cleaned_data['estado_civil']
            data_nasc = form.cleaned_data['data_nasc']
            cep = form.cleaned_data['cep']
            endereco = form.cleaned_data['endereco']
            complemento = form.cleaned_data['complemento']
            numero = form.cleaned_data['numero']
            cidade = form.cleaned_data['cidade']
            bairro = form.cleaned_data['bairro']
            estado = form.cleaned_data['estado']
            tipo_tel = form.cleaned_data['tipo_tel']
            tel = form.cleaned_data['tel']
            # gero codigo uuid para a criação da url de detalhes
            cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Cliente.objects.create(
                    tipo_pessoa = tipo_pessoa,
                    nome = nome,
                    sexo = sexo,
                    cpf_cnpj = cpf_cnpj,
                    rg = rg,
                    email = email,
                    estado_civil = estado_civil,
                    data_nasc = data_nasc,
                    cep = cep,
                    endereco = endereco,
                    complemento = complemento,
                    numero = numero,
                    cidade = cidade,
                    bairro = bairro,
                    estado = estado,
                    tipo_tel = tipo_tel,
                    tel = tel,
                    uuid=cod
                    )
            # em caso de erro
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context = {
                  "titulo":"Cadastro de Clientes",
                  'erro': 'Dados incorretos!'
                }
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/clientes.html", context)
            # se não houver erros redireciono para a lista de clientes
            return HttpResponseRedirect("/clientes/")
        else:
            print('entrou no else')
            # se for um get, renderizo a pagina de cadastro de cliente
            return render(request, "./registration/clientes.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/clientes.html", {"form": UserCreationForm()})


def list_clientes(request):
    """-------------------------------------------------------------------------
    View que lista clientes.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    clientes = Cliente.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'clientes': clientes
    }

    # Retornamos o template no qual os clientes serão dispostos
    return render(request, "clientes.html", context)

def client_details(request, uuid):
    """-------------------------------------------------------------------------
    View que mostra detalhes de cliente.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o cliente
    cliente = Cliente.objects.get(uuid=uuid)

    # Incluímos no contexto
    context = {
      'cliente': cliente
    }
    if request.method == 'POST':
        Cliente.objects.get(uuid=uuid).delete()
        return HttpResponseRedirect("/clientes/")

    # Retornamos o template no qual o cliente será disposto
    return render(request, "./details/clientes.html", context)

def fornecedores(request):
    """-------------------------------------------------------------------------
    View para cadastro de cliente.
    -------------------------------------------------------------------------"""
    context = {
     "titulo":"Cadastro de Fornecedor"
    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            tipo_pessoa = form.cleaned_data['tipo_pessoa']
            nome_fantasia = form.cleaned_data['nome_fantasia']
            nome_fantasia = form.cleaned_data['nome_fantasia']
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            rg_ie = form.cleaned_data['rg_ie']
            email = form.cleaned_data['email']
            data_cadastro = form.cleaned_data['data_cadastro']
            cep = form.cleaned_data['cep']
            endereco = form.cleaned_data['endereco']
            numero = form.cleaned_data['numero']
            cidade = form.cleaned_data['cidade']
            bairro = form.cleaned_data['bairro']
            estado = form.cleaned_data['estado']
            fax = form.cleaned_data['fax']
            tel = form.cleaned_data['tel']
            # gero codigo uuid para a criação da url de detalhes
            cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Fornecedor.objects.create(
                    tipo_pessoa = tipo_pessoa,
                    nome_fantasia = nome_fantasia,
                    cpf_cnpj = cpf_cnpj,
                    rg_ie = rg_ie,
                    email = email,
                    data_cadastro = data_cadastro,
                    cep = cep,
                    endereco = endereco,
                    numero = numero,
                    cidade = cidade,
                    bairro = bairro,
                    estado = estado,
                    fax = fax,
                    tel = tel,
                    uuid = cod
                    )
            # em caso de erro
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context = {
                  "titulo":"Cadastro de Fornecedor",
                  'erro': 'Dados incorretos!'
                }
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/fornecedores.html", context)
            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/fornecedores/")
        else:
            # se for um get, renderizo a pagina de cadastro de fornecedor
            return render(request, "./registration/fornecedores.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/fornecedores.html", {"form": UserCreationForm()})

def list_fornecedores(request):
    """-------------------------------------------------------------------------
    View que lista fornecedores.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    fornecedores = Fornecedor.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'fornecedores': fornecedores
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "fornecedores.html", context)


def forn_details(request, uuid):
    """-------------------------------------------------------------------------
    View que mostra detalhes de fornecedor.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o fornecedor
    fornecedor = Fornecedor.objects.get(uuid=uuid)

    # Incluímos no contexto
    context = {
      'fornecedor': fornecedor
    }
    if request.method == 'POST':
        Fornecedor.objects.get(uuid=uuid).delete()
        return HttpResponseRedirect("/fornecedores/")

    # Retornamos o template no qual o fornecedor será disposto
    return render(request, "./details/fornecedores.html", context)


def pedidos(request):
    context = {
     "titulo":"Cadastro de pedidos"
    }
    return render(request,'registration/pedidos.html',context)


def agendamentos(request):
    context = {
     "titulo":"agendamentos"
    }
    return render(request,'registration/agendamentos.html',context)
