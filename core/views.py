from django.shortcuts import render
from django.http import HttpResponse
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
    context = {}
    return render(request,"login.html",context)
