from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Cliente, Fornecedor, Produto,Pedido,Itens_pedido,Servicos,Agendamentos
from .validations import validaitem
from .forms import ClienteForm, FornecedorForm, ProdutoForm,PedidoForm, AgendamentoForm

#from rest_framework import viewsets
#from .serializers import ProductSerializer

#import uuid

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.error(request,f'Erro ao criar usuário')
                return render(request,'registration/usuario.html',{})
                messages.success(request,f'usuário criado com sucesso!')
            return render(request,'registration/usuario.html',{})
    else:
        form = UserCreationForm()
    return render(request, 'registration/usuario.html', {'form': form})


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
     "titulo":"Cadastro de Produto"
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
            # gero codigo uuid para a criação da url de detalhes
            #cod = uuid.uuid4().hex
            # persisto cliente
            try:
                Produto.objects.create(
                    # id_produto = id_produto,
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
                # print(e)
                # Incluímos no contexto
                context = {
                  "titulo":"Cadastro de Produto",
                  'erro': Exception
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
def updateproduto(request,id):

    produto = Produto.objects.get(id=id)
    produto.custo = str(produto.custo)
    produto.venda = str(produto.venda)
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
    print(cliente)
    if request.method == 'POST':
        print('\n entriuee')
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
            print(form.cleaned_data)
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
    if request.method == 'POST':
        Fornecedor.objects.get(id=id_fornecedor).delete()
        return HttpResponseRedirect("/fornecedores/")

    # Retornamos o template no qual o fornecedor será disposto
    return render(request, "./details/fornecedores.html", context)


@login_required(login_url='/login/')
def pedidos(request):

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    itens_list = []
    """-------------------------------------------------------------------------
    View para cadastro de pedidos.
    -------------------------------------------------------------------------"""
    context = {
            "titulo":"Cadastro de Pedido",
            'clientes': clientes,
            'produtos':produtos,
        }    
    # Se dados forem passados via POST
    if request.method == 'POST':
        #form = ProdutoForm(request.POST)
        # se o formulario for valido
        #if form.is_valid():
        # pego info do form
        id_cli 	=  request.POST.get('id_cliente')
        id_cli  = id_cli.split('-')[0].split(' ')[0]
        pagamento 	=  request.POST.get('pagamento')
        vendedor  	=  request.POST.get('vendedor')
        observacao 	=  request.POST.get('observacao')
        
        for i in range(1,11):
            tipo_prod   =  request.POST.get('tipo_prod'+str(i))
            descricao 	=  request.POST.get('descricao'+str(i))
            quantidade 	=  request.POST.get('quantidade'+str(i))
            unitario = request.POST.get('unitario'+str(i))
            total    = request.POST.get('total')

            if validaitem(tipo_prod,descricao,quantidade,unitario):
                itens_list.append([tipo_prod,descricao,quantidade,unitario])

        # persisto Pedido
        try:
            P = Pedido(
                cliente = id_cli,
                cpf_cnpj=cpf_cnpj,
                tipo=tipo,
                pagamento=pagamento,
                vendedor=vendedor,
                observacao=observacao
                )
            
            P.save()
                
            for item in itens_list:

                I = Itens_pedido(
                    tipo = item[0],
                    descricao = item[1],
                    quantidade = int(item[2]),
                    valor_unitario = float(item[3]),
                    valor_total =  int(item[2]) * float(float(item[3])),
                    pedido = P
                )

                I.save()

        except Exception as e:
            print(e)
            # Incluímos no contexto
            context['erro'] = e
            # retorno a pagina de cadastro com mensagem de erro
            return render(request, "./registration/pedidos.html", context)

        # se não houver erros redireciono para a lista de fornecedores
        return HttpResponseRedirect("/pedidos/")
    else:
        # se for um get, renderizo a pagina de cadastro de fornecedor
        return render(request, "./registration/pedidos.html", context)
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "./registration/pedidos.html", context)


@login_required(login_url='/login/')
def ped_details(request, id_pedido):
    """-------------------------------------------------------------------------
    View que mostra detalhes de pedido.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos o fornecedor
    pedido = Pedido.objects.get(id=id_pedido)
    cliente = Cliente.objects.get(id=pedido.cliente)
    itens_pedido = Itens_pedido.objects.filter(pedido=pedido)
    # Incluímos no contexto
    context = {
      'pedido': pedido,
      'itens_pedido' :itens_pedido,
      'cliente' : cliente
    }
    if request.method == 'POST':
        Pedido.objects.get(id=id_pedido).delete()
        return HttpResponseRedirect("/pedidos/")

    # Retornamos o template no qual o pedido será disposto
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

    servicos = Servicos.objects.all().order_by('-id')

    context = {
    "titulo":"agendamentos",
    "servicos":servicos
    }

    if request.method == "POST":
        dono = request.POST.get("dono")
        pet  = request.POST.get("pet") 
        data = request.POST.get("data")
        hora = request.POST.get("hora")
        servico = request.POST.get("servico")
        print(request.POST)
        form = AgendamentoForm(request.POST)

        if form.is_valid() and hora != '' :
            try:
                serv_id = Servicos.objects.get(descricao=servico)
                Agenda = Agendamentos(
                    proprietario = dono,
                    animal= pet,
                    telefone = '964354314',
                    email = 'rafael.ssilva134@hotmail.com',
                    data = data,
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
    # faço um "SELECT *" ordenado pelo id
    agendamentos = Agendamentos.objects.all().order_by('-id')

    # Incluímos no context
    context = {
      'servicos': agendamentos
    }

    # Retornamos o template no qual os fornecedores serão dispostos
    return render(request, "agendamentos.html", context)

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
        disponivel = request.POST.get("disponibilidade")

        if disponivel == None:
            disponivel = True

        try:
            servico = Servicos(
                descricao = descricao,
                disponivel= disponivel
                )
            servico.save()
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
    context = {
     "titulo":"Deletar servico",
     "servico":servico,
    }

    if request.method == 'POST':

        descricao  = request.POST.get("descricao")
        disponivel = request.POST.get("disponibilidade")

        if disponivel == None:
            disponivel = True
            
        try:
            servico = Servicos(
                descricao = descricao,
                disponivel= disponivel
                )
            
            servico.save()
        except Exception as e:
            # Incluímos no contexto
            context['erro'] = e
            # retorno a pagina de cadastro com mensagem de erro
            return render(request,'registration/servicos.html',context)

    return render(request,'registration/servicedel.html',context)

