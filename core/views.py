from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from .forms import ContatoForm

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


def login(request):
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
            return HttpResponseRedirect("/home/")
        else:
            return render(request, "login.html", {"form": form})

    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "login.html", {"form": AuthenticationForm()})
    #context = {}
    #return render(request,"login.html",context)

def produtos(request):
    context = {
     "titulo":"Cadastro de produtos"
    }
    return render(request,'registration/produtos.html',context)


def clientes(request):
    context = {
     "titulo":"Cadastro de Clientes"
    }
    return render(request,'registration/clientes.html',context)


def fornecedores(request):
    context = {
     "titulo":"Cadastro de fornecedores"
    }
    return render(request,'registration/fornecedores.html',context)


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