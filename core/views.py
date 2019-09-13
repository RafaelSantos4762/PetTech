from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cliente, Fornecedor, Produto,Pedido
from .forms import ClienteForm, FornecedorForm, ProdutoForm

#from rest_framework import viewsets
#from .serializers import ProductSerializer

#import uuid

# Create your views here.

def login_user(request):
    return render(request,'login.html')


@login_required(login_url='/login/')
def logout_user(request):
    logout(request) 
    return redirect('/login/')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                print("O ", username,'é Staff')
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário /ou senha inválidos!')
            return redirect('login.html')


@login_required(login_url='/login/')
def index(request):
    print("==============================================================================")
    print(request)
    print("==============================================================================")
    return render(request,'index.html')


@login_required(login_url='/login/')
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
            id_produto = form.cleaned_data['id_produto']
            cod_bar = form.cleaned_data['cod_bar']
            data_cadastro = form.cleaned_data['data_cadastro']
            descricao = form.cleaned_data['descricao']
            marca = form.cleaned_data['marca']
            custo = form.cleaned_data['custo']
            venda = form.cleaned_data['venda']
            estoque = form.cleaned_data['estoque']
            # gero codigo uuid para a criação da url de detalhes
            #cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Produto.objects.create(
                    id_produto = id_produto,
                    cod_bar = cod_bar,
                    data_cadastro = data_cadastro,
                    descricao = descricao,
                    marca = marca,
                    custo = custo,
                    venda = venda,
                    estoque = estoque,
                    #uuid = cod
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
    return render(request, "./registration/produtos.html", {"form": ProdutoForm()})

@login_required(login_url='/login/')
def list_produtos(request):
    """-------------------------------------------------------------------------
    View que lista produtos.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    try:
        produtos = Produto.objects.all().order_by('-id')
        print(produtos)
    except Exception as e:
        print("-------------------------")
        print(e)
        print("-------------------------")
        
    # Incluímos no context
    context = {
      'produtos': produtos,
    }

    # Retornamos o template no qual os produtos serão dispostos
    return render(request, "produtos.html", context)


@login_required(login_url='/login/')
def prod_details(request,id_produto):
    """-------------------------------------------------------------------------
    View que mostra detalhes de produto.
    -------------------------------------------------------------------------"""

    #Save the template I want to load
    #template = loader.get_template('details/produtos.html')

    # Primeiro, buscamos o produto
    produto = Produto.objects.get(id_produto=int(id_produto))

    # Incluímos no contexto
    context = {
      "produto": produto,
    }
    if request.method == 'POST':
       Produto.objects.get(id_produto=int(id_produto)).delete()

    # Retornamos o template no qual o cliente será disposto
    return render(request, "./details/produtos.html", context)
    #return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def clientes(request):
    """-------------------------------------------------------------------------
    View para cadastro de cliente.
    -------------------------------------------------------------------------"""
    context = {
     "titulo":"Cadastro de Clientes",
     "estados":['SP','SC']
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
            #cod = uuid.uuid4().hex
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
                    tel = tel
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
    return render(request, "./registration/clientes.html", {"form": ClienteForm()})


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def client_details(request, id_cliente):
    """-------------------------------------------------------------------------
    View que mostra detalhes de cliente.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o cliente
    cliente = Cliente.objects.get(id=id_cliente)

    # Incluímos no contexto
    context = {
      'cliente': cliente
    }
    if request.method == 'DELETE':
        Cliente.objects.get(id=id_cliente).delete()
        return HttpResponseRedirect("/clientes/")

    # Retornamos o template no qual o cliente será disposto
    return render(request, "./details/clientes.html", context)


@login_required(login_url='/login/')
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
            #cod = uuid.uuid4().hex
            # persisto fornecedor
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
                    tel = tel
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
    return render(request, "./registration/fornecedores.html", {"form": FornecedorForm()})


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def forn_details(request, id_fornecedor):
    """-------------------------------------------------------------------------
    View que mostra detalhes de fornecedor.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o fornecedor
    fornecedor = Fornecedor.objects.get(id=id_fornecedor)

    # Incluímos no contexto
    context = {
      'fornecedor': fornecedor
    }
    if request.method == 'DELETE':
        Fornecedor.objects.get(id=id_fornecedor).delete()
        return HttpResponseRedirect("/fornecedores/")

    # Retornamos o template no qual o fornecedor será disposto
    return render(request, "./details/fornecedores.html", context)


@login_required(login_url='/login/')
def pedidos(request):

    clientes = Cliente.objects.all().order_by('-id')

    context = {
     "titulo":"Cadastro de pedidos",
     "clientes": clientes
    }
    return render(request,'registration/pedidos.html',context)


@login_required(login_url='/login/')
def ped_details(request, id_pedido):
    """-------------------------------------------------------------------------
    View que mostra detalhes de pedido.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o fornecedor
    pedido = Pedido.objects.get(id=id_pedido)

    # Incluímos no contexto
    context = {
      'fornecedor': fornecedor
    }
    if request.method == 'POST':
        Fornecedor.objects.get(id=id_pedido).delete()
        return HttpResponseRedirect("/pedidos/")

    # Retornamos o template no qual o fornecedor será disposto
    return render(request, "./details/pedidos.html", context)

@login_required(login_url='/login/')
def list_pedidos(request):
    """-------------------------------------------------------------------------
    View que lista pedidos cadastrados.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    pedidos = Pedido.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'pedidos': pedidos
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "pedidos.html", context)

@login_required(login_url='/login/')
def agendamentos(request):
    context = {
     "titulo":"agendamentos"
    }
    return render(request,'registration/agendamentos.html',context)

'''
class getProdutos(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Produto.objects.all()
    serializer_class = ProductSerializer
'''
