from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.utils.timezone import utc
from django.conf import settings
from django.db.models import Sum

from .models import *
from .validations import validaitem
from .forms import ClienteForm, FornecedorForm, ProdutoForm,PedidoForm, AgendamentoForm

#from rest_framework import viewsets
#from .serializers import ProductSerializer


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.error(request,f'Erro ao criar usuário')
                return render(request,'registration/usuarios.html',{})
                messages.success(request,f'usuário criado com sucesso!')
            return render(request,'registration/usuarios.html',{})
    else:
        form = UserCreationForm()
    return render(request, 'registration/usuarios.html', {'form': form})


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
            return render(request,'login.html')


@login_required(login_url='/login/')
def index(request):
    print("==============================================================================")
    print(request)
    print("==============================================================================")
    return render(request,'index.html', {'logo': True})


@login_required(login_url='/login/')
def produtos(request):
    """-------------------------------------------------------------------------
    View para cadastro de produto.
    -------------------------------------------------------------------------"""
    context = {
     'form': ProdutoForm(),
     "titulo":"Cadastro de Produto",
     'data_cadastro': date.today().strftime('%Y-%m-%d')
    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            # id_produto = form.cleaned_data['id_produto']
            cod_bar = form.cleaned_data['cod_bar']
            if cod_bar is None:
                cod_bar=''
            data_cadastro = form.cleaned_data['data_cadastro']
            descricao = form.cleaned_data['descricao']
            marca = form.cleaned_data['marca']

            # gero codigo uuid para a criação da url de detalhes
            #cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Produto.objects.create(
                    # id_produto = id_produto,
                    cod_bar = cod_bar,
                    data_cadastro = data_cadastro,
                    descricao = descricao,
                    marca = marca
                    )
            # em caso de erro
            except Exception as exce:
                
                # Incluímos no contexto
                context = {
                  "titulo":"Cadastro de Produto",
                  'erro': "erro"
                }
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/produtos.html", context)
            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/produtos/")
    
    context['form'] = ProdutoForm()
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/produtos.html", context)

@login_required(login_url='/login/')
def updateproduto(request,id):

    produto = Produto.objects.get(id=id)
    #produto.custo = str(produto.custo)
    #produto.venda = str(produto.venda)
    produto.data_cadastro = str(produto.data_cadastro.year) +'-'+ str(produto.data_cadastro.month) +'-'+ str(produto.data_cadastro.day)

    context = {
     "titulo":"Atualizacao de Produto",
     'produto':produto

    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            # id_produto = form.cleaned_data['id_produto']
            cod_bar = form.cleaned_data['cod_bar']
            if cod_bar is None:
                cod_bar=''
            data_cadastro = form.cleaned_data['data_cadastro']
            descricao = form.cleaned_data['descricao']
            marca = form.cleaned_data['marca']
            custo = form.cleaned_data['custo']
            venda = form.cleaned_data['venda']
            estoque = form.cleaned_data['estoque']

            try:
                produto.cod_bar = cod_bar
                produto.descricao = descricao
                produto.marca = marca
                produto.custo = custo
                produto.venda = venda
                produto.estoque = estoque

                produto.save()
            except Exception as e:

                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./update/produtos.html", context)
            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/produtos/")
    form = ProdutoForm()
    
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./update/produtos.html", context)

@login_required(login_url='/login/')
def list_produtos(request):
    """-------------------------------------------------------------------------
    View que lista produtos.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id

    search = request.GET.get('search')

    if search:
        prods_list = Produto.objects.filter(descricao__icontains=search)
        if len(prods_list) == 0:
            prods_list = Produto.objects.filter(id__icontains=search)
    else:

        prods_list = Produto.objects.all().order_by('-id')

    paginator = Paginator(prods_list, 5)

    page = request.GET.get('page')

    produtos = paginator.get_page(page)

    context = {
    'produtos': produtos,
    'placehld': 'Digite a descrição ou ID do produto que deseja buscar...',
    'titulo' : 'Lista de produtos',
    }        
    # Retornamos o template no qual os produtos serão dispostos
    return render(request, "produtos.html", context)



@login_required(login_url='/login/')
def prod_details(request,id):
    """-------------------------------------------------------------------------
    View que mostra detalhes de produto.
    -------------------------------------------------------------------------"""

    #Save the template I want to load
    #template = loader.get_template('details/produtos.html')

    # Primeiro, buscamos o produto
    produto = Produto.objects.get(id=int(id))

    # Incluímos no contexto
    context = {
      "produto": produto,
    }
    if request.method == 'POST':
       Produto.objects.get(id=int(id)).delete()
       return HttpResponseRedirect("/produtos/")

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
def updatecliente(request, id):

    cliente = Cliente.objects.get(pk=id)
    cliente.data_nasc = str(cliente.data_nasc.year) +'-'+ str(cliente.data_nasc.month) +'-'+ str(cliente.data_nasc.day)

    print(cliente)
    context = {
     "titulo":"Alteração de Clientes",
     'cliente': cliente,
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
                
                cliente.tipo_pessoa = tipo_pessoa
                cliente.nome = nome
                cliente.sexo = sexo
                cliente.cpf_cnpj = cpf_cnpj
                cliente.rg = rg
                cliente.email = email
                cliente.estado_civil = estado_civil
                cliente.data_nasc = data_nasc
                cliente.cep = cep
                cliente.endereco = endereco
                cliente.complemento = complemento
                cliente.numero = numero
                cliente.cidade = cidade
                cliente.bairro = bairro
                cliente.estado = estado
                cliente.tipo_tel = tipo_tel
                cliente.tel = tel

                cliente.save()    
            # em caso de erro
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./update/clientes.html", context)
            # se não houver erros redireciono para a lista de clientes
            return HttpResponseRedirect("/clientes/")
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./update/clientes.html",context)


@login_required(login_url='/login/')
def list_clientes(request):
    """-------------------------------------------------------------------------
    View que lista clientes.
    -------------------------------------------------------------------------"""
    search = request.GET.get('search')

    if search:
        clientes_list = Cliente.objects.filter(nome__icontains=search) | Cliente.objects.filter(id__icontains=search)
        clientes_list.order_by('-id')
    else:
        clientes_list = Cliente.objects.all().order_by('-id')

    paginator = Paginator(clientes_list, 5)

    page = request.GET.get('page')

    clientes = paginator.get_page(page)

    print('clientes recebidos',clientes)

    # Incluímos no context
    context = {
      'clientes': clientes,
      'placehld': 'Digite a descrição ou ID do cliente que deseja buscar...',
      'titulo': 'Lista de clientes',
    }
    # Retornamos o template no qual os produtos serão dispostos

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
    print(cliente)
    if request.method == 'POST':
        cliente.delete()
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
            razao_social = form.cleaned_data['razao_social']
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
                    razao_social = razao_social,
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
            print(form.cleaned_data)
            return render(request, "./registration/fornecedores.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/fornecedores.html", {"form": FornecedorForm()})

@login_required(login_url='/login/')
def updatefornecedor(request,id):

    estados = []
    fornecedor = Fornecedor.objects.get(pk=id)
    fornecedor.data_cadastro = str(fornecedor.data_cadastro.year) +'-'+ str(fornecedor.data_cadastro.month) +'-'+ str(fornecedor.data_cadastro.day)
    cgc_bkp = fornecedor.cpf_cnpj
    #fornecedor.cpf_cnpj = fornecedor.cpf_cnpj[:2] + '.' + fornecedor.cpf_cnpj[2:5] + '.' + fornecedor.cpf_cnpj[5:8] + '/' + fornecedor.cpf_cnpj[8:12] + '-' + fornecedor.cpf_cnpj[12:14]
    
    estados.append('AC')
    estados.append('AL')
    estados.append('AP')
    estados.append('AM')
    estados.append('BA')
    estados.append('CE')
    estados.append('DF')
    estados.append('ES')
    estados.append('GO')
    estados.append('MA')
    estados.append('MT')
    estados.append('MS')
    estados.append('MG')
    estados.append('PA')
    estados.append('PB')
    estados.append('PR')
    estados.append('PE')
    estados.append('PI')
    estados.append('RJ')
    estados.append('RN')
    estados.append('RS')
    estados.append('RO')
    estados.append('RR')
    estados.append('SC')
    estados.append('SP')
    estados.append('SE')
    estados.append('TO')

    context = {
     "titulo":"Atualização de Fornecedor",
     'fornecedor' : fornecedor,
     'estados' : estados
    }
    # Se dados forem passados via POST
    if request.method == 'POST':
        #fornecedor.cpf_cnpj = cgc_bkp
        form = FornecedorForm(request.POST)
        if form.is_valid():
            # pego info do form
            tipo_pessoa = form.cleaned_data['tipo_pessoa']
            nome_fantasia = form.cleaned_data['nome_fantasia']
            razao_social = form.cleaned_data['razao_social']
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

            try:
                
                fornecedor.tipo_pessoa = tipo_pessoa
                fornecedor.nome_fantasia = nome_fantasia
                fornecedor.razao_social = razao_social
                fornecedor.cpf_cnpj = cpf_cnpj
                fornecedor.rg_ie = rg_ie
                fornecedor.email = email
                fornecedor.data_cadastro = data_cadastro
                fornecedor.cep = cep
                fornecedor.endereco = endereco
                fornecedor.numero = numero
                fornecedor.cidade = cidade
                fornecedor.bairro = bairro
                fornecedor.estado = estado
                fornecedor.fax = fax
                fornecedor.tel = tel

                fornecedor.save()
            # em caso de erro
            except Exception as e:
                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./update/fornecedores.html", context)
            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/fornecedores/")

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./update/fornecedores.html", context)


@login_required(login_url='/login/')
def list_fornecedores(request):
    """-------------------------------------------------------------------------
    View que lista fornecedores.
    -------------------------------------------------------------------------"""
    search = request.GET.get('search')

    if search:
        fornece_list = Fornecedor.objects.filter(razao_social__icontains=search) | Fornecedor.objects.filter(id__icontains=search)
        fornece_list.order_by('-id')
    else:
        fornece_list = Fornecedor.objects.all().order_by('-id')

    paginator = Paginator(fornece_list, 5)

    page = request.GET.get('page')

    fornecedores = paginator.get_page(page)

    # Incluímos no context
    context = {
      'fornecedores': fornecedores,
      'placehld': 'Digite a descrição ou ID do fornecedor que deseja buscar...',
      'titulo': 'Lista de Fornecedores',
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
    if request.method == 'POST':
        Fornecedor.objects.get(id=id_fornecedor).delete()
        return HttpResponseRedirect("/fornecedores/")

    # Retornamos o template no qual o fornecedor será disposto
    return render(request, "./details/fornecedores.html", context)

def verifica_item_pedido(request):
    descricao 	=  request.POST.get('descricao1')
    quantidade 	=  request.POST.get('quantidade1')
    unitario = request.POST.get('unitario1')
    return (descricao != None and descricao != '') and (quantidade != None and quantidade != '') and (unitario != None and unitario != '')


@login_required(login_url='/login/')
def pedido_venda(request):

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    formas   = Tipos_pagamento.objects.all()
    itens_list = {}
    itens = []
    """-------------------------------------------------------------------------
    View para cadastro de pedidos.
    -------------------------------------------------------------------------"""
    context = {
            "titulo":"Cadastro de Pedido",
            'clientes': clientes,
            'produtos':produtos,
            'formas': formas
        }    
    # Se dados forem passados via POST
    if request.method == 'POST':
        
        form = PedidoForm(request.POST)
        
        if form.is_valid():

            id_cli 	=  int(request.POST.get('cliente'))
            tipo 	=  request.POST.get('tipo')
            vendedor  	=  request.POST.get('vendedor')
            observacao 	=  request.POST.get('observacao')
            cgc = Cliente.objects.get(pk=id_cli).cpf_cnpj
            pagamento = int(request.POST.get('pagamento'))
            
            itens_list['descricao'] = request.POST.getlist('descricao')
            itens_list['quantidade'] = request.POST.getlist('quantidade')
            itens_list['unitario'] = request.POST.getlist('unitario')
            #itens_list['total'] = request.POST.getlist('total')

            #Defino a quantidade de itens baseado no campo quantidade
            total_itens = len(itens_list['quantidade'] )            

            # persisto Pedido
            try:
                forma_pagamento = Tipos_pagamento.objects.get(pk=pagamento)
                descri_pg = forma_pagamento.descricao
                P = Pedido(
                    cliente = id_cli,
                    cpf_cnpj = cgc,
                    tipo=tipo,
                    pagamento=forma_pagamento,
                    forma_pagamento=descri_pg,
                    vendedor=vendedor,
                    observacao=observacao,
                    )
                
                P.save()
                    
                for item in range(0,total_itens):
                    
                    prod = Produto.objects.get(pk=int(itens_list['descricao'][item]))

                    descricao = prod.descricao
                    quantidade = int(itens_list['quantidade'][item])
                    unitario   = float(itens_list['unitario'][item].replace(',','.'))

                    if validaitem(descricao,quantidade,unitario):

                        I = Itens_pedido(
                            produto = prod,
                            descricao = descricao,
                            quantidade = quantidade,
                            valor_unitario = unitario,
                            valor_total =  quantidade * unitario,
                            pedido = P
                        )

                        I.save()
                    
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/pedido_venda.html", context)

            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/pedidos/pendentes/")
        else: 
            context['form'] = form
            if not(verifica_item_pedido(request)):
                context['item_error'] = 'Obrigatório pelo menos 1 item!'
            return render(request, "./registration/pedido_venda.html", context) 
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/pedido_venda.html", context)

@login_required(login_url='/login/')
def pedido_compra(request):

    fornecedor = Fornecedor.objects.all()
    produtos = Produto.objects.all()
    formas   = Tipos_pagamento.objects.all()
    itens_list = {}
    itens = []
    """-------------------------------------------------------------------------
    View para cadastro de pedidos.
    -------------------------------------------------------------------------"""
    context = {
            "titulo":"Cadastro de Pedido",
            'fornecedores': fornecedor,
            'produtos':produtos,
            'formas': formas
        }    
    # Se dados forem passados via POST
    if request.method == 'POST':
        #form = ProdutoForm(request.POST)
        # se o formulario for valido
        #if form.is_valid():
        # pego info do form

        form = PedidoForm(request.POST)

        if form.is_valid():

            id_fornece 	=  int(request.POST.get('cliente'))
            tipo 	=  request.POST.get('tipo')
            vendedor  	=  request.POST.get('vendedor')
            observacao 	=  request.POST.get('observacao')
            cgc = Fornecedor.objects.get(pk=id_fornece).cpf_cnpj
            pagamento = int(request.POST.get('pagamento'))

            itens_list['descricao'] = request.POST.getlist('descricao')
            itens_list['quantidade'] = request.POST.getlist('quantidade')
            itens_list['unitario'] = request.POST.getlist('unitario')
            #itens_list['total'] = request.POST.getlist('total')

            #Defino a quantidade de itens baseado no campo quantidade
            total_itens = len(itens_list['quantidade'] )            
        
            # persisto Pedido
            try:
                forma_pagamento = Tipos_pagamento.objects.get(pk=pagamento)
                descri_pg = forma_pagamento.descricao
                P = Pedido(
                    cliente = id_fornece,
                    cpf_cnpj = cgc,
                    tipo=tipo,
                    pagamento=forma_pagamento,
                    forma_pagamento=descri_pg,
                    vendedor=vendedor,
                    observacao=observacao,
                    )
                
                P.save()
                    
                for item in range(0,total_itens):
                    
                    prod = Produto.objects.get(pk=int(itens_list['descricao'][item]))
                    descricao = prod.descricao
                    quantidade = int(itens_list['quantidade'][item])
                    unitario   = float(itens_list['unitario'][item].replace(',','.'))

                    if validaitem(descricao,quantidade,unitario):

                        I = Itens_pedido(
                            produto = prod,
                            descricao = descricao,
                            quantidade = quantidade,
                            valor_unitario = unitario,
                            valor_total =  quantidade * unitario,
                            pedido = P
                        )

                        I.save()
                    
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "./registration/pedido_compra.html", context)

            # se não houver erros redireciono para a lista de fornecedores
            return HttpResponseRedirect("/pedidos/pendentes/")
        else: 
            context['form'] = form
            if not(verifica_item_pedido(request)):
                context['item_error'] = 'Obrigatório pelo menos 1 item!'
            return render(request, "./registration/pedido_compra.html", context) 
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/pedido_compra.html", context)


@login_required(login_url='/login/')
def ped_details_aprovado(request, id_pedido):
    """-------------------------------------------------------------------------
    View que mostra detalhes de pedido.
    -------------------------------------------------------------------------"""
    pedido = Pedido.objects.get(id=id_pedido)
    venda = pedido.tipo.strip().upper() == "VENDA"

    if venda:
        cliente = Cliente.objects.get(id=pedido.cliente)
    else:
        cliente = Fornecedor.objects.get(id=pedido.cliente)
    if len(cliente.cpf_cnpj.strip()) > 11:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:2] + '.' + cliente.cpf_cnpj[2:5] + '.' + cliente.cpf_cnpj[5:8] + '/' + cliente.cpf_cnpj[8:12] + '-' + cliente.cpf_cnpj[12:14]
    else:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:3] + '.' + cliente.cpf_cnpj[3:6] + '.' + cliente.cpf_cnpj[6:9] + '-' + cliente.cpf_cnpj[9:11] 

    itens_pedido = Itens_pedido.objects.filter(pedido=pedido)
    # Incluímos no contexto
    context = {
      'pedido': pedido,
      'itens_pedido' :itens_pedido,
      'cliente' : cliente,
      'venda': venda,
    }
    if request.method == 'POST':
        Pedido.objects.get(id=id_pedido).delete()
        return HttpResponseRedirect("/pedidos/pendentes/")

    return render(request, "./details/pedidos.html", context)

@login_required(login_url='/login/')
def ped_details_pendente(request, id_pedido):
    """-------------------------------------------------------------------------
    View que mostra detalhes de pedido.
    -------------------------------------------------------------------------"""
    
    pedido = Pedido.objects.get(id=id_pedido)
    venda = pedido.tipo.strip().upper() == "VENDA"

    if venda:
        cliente = Cliente.objects.get(id=pedido.cliente)
    else:
        cliente = Fornecedor.objects.get(id=pedido.cliente)
    if len(cliente.cpf_cnpj.strip()) > 11:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:2] + '.' + cliente.cpf_cnpj[2:5] + '.' + cliente.cpf_cnpj[5:8] + '/' + cliente.cpf_cnpj[8:12] + '-' + cliente.cpf_cnpj[12:14]
    else:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:3] + '.' + cliente.cpf_cnpj[3:6] + '.' + cliente.cpf_cnpj[6:9] + '-' + cliente.cpf_cnpj[9:11] 

    itens_pedido = Itens_pedido.objects.filter(pedido=pedido)
    # Incluímos no contexto
    context = {
      'pedido': pedido,
      'itens_pedido' :itens_pedido,
      'cliente' : cliente,
      'venda': venda,
    }
    if request.method == 'POST':
        Pedido.objects.get(id=id_pedido).delete()
        return HttpResponseRedirect("/pedidos/pendentes/")

    # Retornamos o template no qual o pedido será disposto
    return render(request, "./details/pedidos.html", context)

@login_required(login_url='/login/')
def pedidos_pendentes(request):
    """-------------------------------------------------------------------------
    View que lista pedidos cadastrados.
    -------------------------------------------------------------------------"""

    search = request.GET.get('search')

    if search:
        pedidos_ist = Pedido.objects.filter(id__icontains=search,efetivado=False)
        pedidos_ist.order_by('-id')
    else:
        pedidos_ist = Pedido.objects.filter(efetivado=False).order_by('-id')

    paginator = Paginator(pedidos_ist, 5)

    page = request.GET.get('page')

    pedidos = paginator.get_page(page)

    aprovado = False

    for pedido in pedidos:
        if pedido.tipo.strip().upper() == "Venda":
            cli_forn = Cliente.objects.get(pk=pedido.cliente)
            pedido.cliente = cli_forn.nome
        else:
            cli_forn = Fornecedor.objects.get(pk=pedido.cliente)
            pedido.cliente = cli_forn.razao_social

    # Incluímos no context
    context = {
      'pedidos': pedidos,
      'placehld': 'Digite o nome do cliente ou ID do pedido que deseja buscar...',
      'titulo': 'Pedidos pendentes de aprovação',
      'aprovado' : aprovado,
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "pedidos.html", context)


@login_required(login_url='/login/')
def pedidos_aprovados(request):
    """-------------------------------------------------------------------------
    View que lista pedidos cadastrados.
    -------------------------------------------------------------------------"""

    search = request.GET.get('search')
    aprovado = 'APROVADO' in request.path.upper()

    if search:
        pedidos_ist = Pedido.objects.filter(id__icontains=search,efetivado=True)
        pedidos_ist.order_by('-id')
    else:
        pedidos_ist = Pedido.objects.filter(efetivado=True).order_by('-id')

    paginator = Paginator(pedidos_ist, 5)

    page = request.GET.get('page')

    pedidos = paginator.get_page(page)

    # Incluímos no context
    context = {
      'pedidos': pedidos,
      'placehld': 'Digite o nome do cliente ou ID do pedido que deseja buscar...',
      'titulo': 'Pedidos aprovados',
      'aprovado' : aprovado,
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "pedidos.html", context)

@login_required(login_url='/login/')
def efetivar_pedido(request,id):
    pedido = Pedido.objects.get(pk=id)

    if pedido.tipo.strip().upper() == "VENDA":
        cliente = Cliente.objects.get(id=pedido.cliente)
    else:
        cliente = Fornecedor.objects.get(pk=pedido.cliente)

    pagamento = Tipos_pagamento.objects.get(pk=pedido.pagamento_id)
    #mensagens = message.get.messages(request)
    if len(cliente.cpf_cnpj.strip()) > 11:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:2] + '.' + cliente.cpf_cnpj[2:5] + '.' + cliente.cpf_cnpj[5:8] + '/' + cliente.cpf_cnpj[8:12] + '-' + cliente.cpf_cnpj[12:14]
    else:
        cliente.cpf_cnpj = cliente.cpf_cnpj[:3] + '.' + cliente.cpf_cnpj[3:6] + '.' + cliente.cpf_cnpj[6:9] + '-' + cliente.cpf_cnpj[9:11] 
    
    itens_pedido = Itens_pedido.objects.filter(pedido_id=pedido.id)
    # Incluímos no contexto
    context = {
      'pedido': pedido,
      'itens_pedido' :itens_pedido,
      'cliente' : cliente,
      'pagamento': pagamento,  
    }

    if request.method == 'POST':

        for item in itens_pedido:
            entrada = True
            if pedido.tipo.strip().upper() == "VENDA":
                entrada = False

            saldo = item.quantidade
                
            produto = Produto.objects.get(id=item.produto.id)
   
            try:    
                estoque = Estoque.objects.get(produto_id=produto.id)
            except:
                if not entrada:#Venda
                    messages.error(request, f'Saldo do produto "{produto.id} - {produto.descricao}" insuficiente.')
                    messages.error(request, f'Favor verificar o estoque!')
                    context['messagens'] = messages
                    return redirect(request.path)                    
                else:#Compra
                    estoque = Estoque(produto_id = produto.id,quantidade = saldo)
                    estoque.save()
                    pedido.efetivado = True
                    pedido.save()                

                    entrada =  Entrada(
                        fornecedor = cliente,
                        fornecedor_nome = cliente.raza_social,
                        Pedido = pedido,
                        produto = produto,
                        produto_descricao = produto.descricao,
                        quantidade = item.quantidade,
                        valor_unitario = item.valor_unitario,
                        valor_total = item.valor_total
                        )
                    entrada.save()

            if not entrada:#Venda
                if item.quantidade > estoque.quantidade:
                    messages.error(request, f'Saldo do produto "{produto.id} - {produto.descricao}" insuficiente.')
                    messages.error(request, f'Favor verificar o estoque!')
                    context['messagens'] = messages
                    return redirect(request.path)
                else:
                    estoque.quantidade = estoque.quantidade - saldo
                    saida =  Saida(
                        cliente = cliente,
                        cliente_nome = cliente.nome,
                        Pedido = pedido,
                        produto = produto,
                        produto_descricao = produto.descricao,
                        quantidade = item.quantidade,
                        valor_unitario = item.valor_unitario,
                        valor_total = item.valor_total
                        )
                    saida.save()
                    
            else:#Compra
                estoque.quantidade = estoque.quantidade + saldo
            estoque.save()
            pedido.efetivado = True
            pedido.save()
        #Define pedido como efetivado e remove da lista de pendentes        
        return redirect("/pedidos/aprovados/")

    # Retornamos o template no qual o pedido será disposto
    return render(request, 'efetivar/pedido.html', context)

@login_required(login_url='/login/')
def agendamentos(request):

    servicos = Servicos.objects.filter(disponivel=1).order_by('-id')

    context = {
    "titulo":"Agendamentos",
    "servicos":servicos
    }

    if request.method == "POST":

        form = AgendamentoForm(request.POST)

        if form.is_valid():

            dono = form.cleaned_data['dono']
            pet  = form.cleaned_data['pet']
            data = form.cleaned_data['data']
            hora = form.cleaned_data['hora']
            servico = int(form.cleaned_data['servico'])
            dia = data.strftime("%A")

            try:
                
                serv_id = Servicos.objects.get(pk=servico)
                Agenda = Agendamentos(
                    proprietario = dono,
                    animal= pet,
                    telefone = '964354314',
                    email = 'rafael.ssilva134@hotmail.com',
                    data = data,
                    dia = dia,
                    hora = hora,
                    servico = serv_id,
                    serv_desc = servico
                    )
                
                Agenda.save()

            except Exception as e:
                # Incluímos no contexto
                context['erro'] = e
                # retorno a pagina de cadastro com mensagem de erro
                return render(request,'registration/agendamentos.html',context)

            return HttpResponseRedirect("/agendamentos/")
        else: 
            context['form'] = form
            return render(request, 'registration/agendamentos.html', context )


    return render(request,'registration/agendamentos.html',context)

@login_required(login_url='/login/')
def list_agendamentos(request):
    """-------------------------------------------------------------------------
    View que lista os serviços disponíveis.
    -------------------------------------------------------------------------"""
    dias = {
        "SUNDAY":"DOMINGO",
        "MONDAY":"SEGUNDA", 
        "TUESDAY":"TERCA",
        "WEDNESDAY":"QUARTA",
        "THURSDAY":"QUINTA", 
        "FRIDAY":"SEXTA", 
        "SATURDAY":"SABADO"
        }

    meses = {
        'JANUARY':'JANEIRO',
        'FEBURARY':'FEVEREIRO',
        'MARCH':'MARÇO',
        'APRIL':'ABRIL',
        'MAY':'MAIO',
        'JUNE':'JUNHO',
        'JULY':'JULHO',
        'AUGUST':'AGOSTO',
        'SEPTEMBER':'SETEMBRO',
        'OCTOBER':'OUTUBRO',
        'NOVEMBER':'NOVEMBRO',
        'DECEMBER':'DEZEMBRO',

    }

    #Monto esttutura dos dias da semana.
    primeiro = datetime.utcnow().replace(tzinfo=utc)
    primeiro = dias[primeiro.strftime("%A").strip().upper()].capitalize() + ' ' + primeiro.strftime("%d").strip().upper() + ' ' + meses[primeiro.strftime("%B").strip().upper()]
    segundo =  datetime.now() + timedelta(days=1)
    segundo = dias[segundo.strftime("%A").strip().upper()].capitalize()  + ' ' + segundo.strftime("%d").strip().upper() + ' ' + meses[segundo.strftime("%B").strip().upper()]
    terceiro = datetime.now() + timedelta(days=2) 
    terceiro = dias[terceiro.strftime("%A").strip().upper()].capitalize() + ' ' + terceiro.strftime("%d").strip().upper() + ' ' + meses[terceiro.strftime("%B").strip().upper()]
    quarto =   datetime.now() + timedelta(days=3)
    quarto = dias[quarto.strftime("%A").strip().upper()].capitalize() + ' ' + quarto.strftime("%d").strip().upper() + ' ' + meses[quarto.strftime("%B").strip().upper()]
    quinto =   datetime.now() + timedelta(days=4)
    quinto = dias[quinto.strftime("%A").strip().upper()].capitalize() + ' ' + quinto.strftime("%d").strip().upper() + ' ' + meses[quinto.strftime("%B").strip().upper()]
    sexto =    datetime.now() + timedelta(days=5)
    sexto = dias[sexto.strftime("%A").strip().upper()].capitalize() + ' ' + sexto.strftime("%d").strip().upper() + ' ' + meses[sexto.strftime("%B").strip().upper()]
    setimo =   datetime.now() + timedelta(days=6)
    setimo = dias[setimo.strftime("%A").strip().upper()].capitalize()  + ' ' + setimo.strftime("%d").strip().upper() + ' ' + meses[setimo.strftime("%B").strip().upper()]

    dia1 = datetime.now().day
    dia2 = (datetime.now() + timedelta(days=1)).day
    dia3 = (datetime.now() + timedelta(days=2)).day
    dia4 = (datetime.now() + timedelta(days=3)).day
    dia5 = (datetime.now() + timedelta(days=4)).day
    dia6 = (datetime.now() + timedelta(days=5)).day
    dia7 = (datetime.now() + timedelta(days=6)).day

    # faço um "SELECT *" ordenado pelo id
    agendamentos = Agendamentos.objects.filter(data__gte=datetime.now() ,data__lte=datetime.now() + timedelta(days=6)).order_by('hora')

    # Incluímos no context
    context = {
      'agendamentos': agendamentos,
      "primeiro":primeiro,
      "segundo":segundo,
      "terceiro": terceiro,
      "quarto": quarto,
      "quinto":quinto,
      "sexto":sexto,
      "setimo":setimo,
      'dia1': dia1,
      'dia2': dia2,
      'dia3': dia3,
      'dia4': dia4,
      'dia5': dia5,
      'dia6': dia6,
      'dia7': dia7
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "consultas/agendamentos.html", context)

@login_required(login_url='/login/')
def agendamento_details(request, id_servico):
    """-------------------------------------------------------------------------
    View que mostra detalhes de agendamento.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o fornecedor
    agendamentos = Agendamentos.objects.get(id=id_servico)

    # Incluímos no contexto
    context = {
      'agendamento': agendamentos,
    }
    if request.method == 'POST':
        Agendamentos.objects.get(id=id_servico).delete()
        return HttpResponseRedirect("/agendamentos/")

    # Retornamos o template no qual o pedido será disposto
    return render(request, "./details/agendamentos.html", context)

'''
class getProdutos(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Produto.objects.all()
    serializer_class = ProductSerializer
'''

@login_required(login_url='/login/')
def servicos(request):

    context = {
     "titulo":"serviços",
    }

    if request.method == 'POST':
        descricao  = request.POST.get("descricao")
        disponivel = request.POST.get("ativo").upper() == "SIM"

        try:
            servico = Servicos(
                descricao = descricao,
                disponivel= disponivel
                )
            servico.save()
            return redirect("/servicos/")
        except Exception as e:
            # Incluímos no contexto
            context['erro'] = e
            # retorno a pagina de cadastro com mensagem de erro
            return render(request,'registration/servicos.html',context)

    return render(request,'registration/servicos.html',context)


@login_required(login_url='/login/')
def list_servicos(request):
    """-------------------------------------------------------------------------
    View que lista os serviços disponíveis.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pelo id
    servicos = Servicos.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'servicos': servicos
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "servicos.html", context)



@login_required(login_url='/login/')
def deleteservico(request,id_servico):

    servico = Servicos.objects.get(id=id_servico)

    servico_id = servico.id
    servico_nome = servico.descricao

    if request.method == 'POST':

        servico.delete()

        messages.success(request,f'Serviço [{servico_id} - {servico_nome}] deletado com sucesso!')

        # retorno a pagina de cadastro com mensagem de erro
        return redirect('/servicos/')
    messages.success(request,f'Foi um get')
    return redirect('/servicos/')

@login_required(login_url='/login/')
def consultar_saldos(request):

    search = request.GET.get('search')

    if search:
        saldos_list = Estoque.objects.select_related('produto').filter(produto__descricao__icontains=search) or Estoque.objects.select_related('produto').filter(produto__id__icontains=search) 
        #fornece_list = Fornecedor.objects.filter(razao_social__icontains=search) | Fornecedor.objects.filter(id__icontains=search)
        #fornece_list.order_by('-id')
    else:
        saldos_list = Estoque.objects.select_related('produto')

    paginator = Paginator(saldos_list, 5)

    page = request.GET.get('page')

    saldos = paginator.get_page(page)    

    context = {
        'titulo': 'Saldos de produtos disponíveis',
        'saldos': saldos,
        'placehld': 'Digite o nome do produto ou ID para buscar.'
    }

    return render(request, 'consultas/saldos.html', context)


@login_required(login_url='/login/')
def consultar_saidas(request):

    search = request.GET.get('search')

    if search:
        consulta_list = Itens_pedido.objects.select_related().filter(pedido__tipo="Venda", produto__descricao__icontains=search).order_by('-id')
        #fornece_list = Fornecedor.objects.filter(razao_social__icontains=search) | Fornecedor.objects.filter(id__icontains=search)
        #fornece_list.order_by('-id')
    else:
        consulta_list = Itens_pedido.objects.select_related().filter(pedido__tipo="Venda").order_by('-id')

    paginator = Paginator(consulta_list, 5)

    page = request.GET.get('page')

    consultas = paginator.get_page(page)    

    context = {
        'titulo': 'Resumo de vendas',
        'consultas': consultas,
        'placehld': 'Digite o nome do produto para buscar.'
    }

    return render(request, 'consultas/saidas.html', context)


@login_required(login_url='/login/')
def consultar_entradas(request):

    search = request.GET.get('search')

    if search:
        consulta_list = Itens_pedido.objects.select_related().filter(pedido__tipo="Compra", produto__descricao__icontains=search).order_by('-id')
        #fornece_list = Fornecedor.objects.filter(razao_social__icontains=search) | Fornecedor.objects.filter(id__icontains=search)
        #fornece_list.order_by('-id')
    else:
        consulta_list = Itens_pedido.objects.select_related().filter(pedido__tipo="Compra").order_by('-id')

    paginator = Paginator(consulta_list, 5)

    page = request.GET.get('page')

    consultas = paginator.get_page(page)    

    context = {
        'titulo': 'Resumo de compras',
        'consultas': consultas,
        'placehld': 'Digite o nome do produto para buscar.'
    }

    return render(request, 'consultas/saidas.html', context)


def register_formas(request):

    context = {
        'titulo': 'Cadastro de formas de pagamento'
    }

    if request.method == "POST":
        descricao = request.POST.get('descricao')
        try:
            P = Tipos_pagamento(descricao=descricao)
            P.save()
        except Exception as erro:
            context['erro'] = erro

    return render(request, 'registration/formas_pagamento.html', context)