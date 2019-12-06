from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cliente(models.Model):
    tipo_pessoa = models.CharField(max_length=20)
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=20)
    cpf_cnpj = models.CharField(max_length=14)
    rg = models.CharField(max_length=10)
    email = models.EmailField()
    estado_civil = models.CharField(max_length=10)
    data_nasc = models.DateField()
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=200)
    complemento = models.CharField(max_length=100)
    numero = models.CharField(max_length=6)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=60)
    estado = models.CharField(max_length=40)
    tipo_tel = models.CharField(max_length=10)
    tel = models.CharField(max_length=10)
    #uuid = models.CharField(default='-- -- --', max_length=300)
    #url = models.URLField(default='-- -- --', max_length=300)

    def save(self, *args, **kwargs):
        
        #Validação do objeto.
        
        TIPO_PESSOA = ['Fisica', 'Juridica']
        SEXO = ['Masculino', 'Feminino']
        ESTADO_CIVIL = [
                        'Solteiro(a)',
                        'Casado(a)',
                        'Divorciado(a)',
                        'Víuvo(a)'
                        ]
        ESTADO = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
                "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                ]
        TIPO_TEL = ['Residencial', 'Celular', 'Comercial']

        if self.tipo_pessoa not in TIPO_PESSOA:
            raise Exception('Campo Tipo Pessoa Inválido!')
        if self.sexo not in SEXO:
            raise Exception('Campo Sexo Inválido!')
        #if self.estado_civil not in ESTADO_CIVIL:
         #   raise Exception('Campo Estado Civil Inválido!')
        if self.estado not in ESTADO:
            raise Exception('Campo Estado Inválido!')
        if self.tipo_tel not in TIPO_TEL:
            raise Exception('Campo Tipo de Telefone Inválido!')
        #self.url = f'/cliente/details/{self.uuid}/'
        super(Cliente, self).save(*args, **kwargs)


class Fornecedor(models.Model):
    tipo_pessoa = models.CharField(max_length=200)
    data_cadastro = models.DateField()
    nome_fantasia = models.CharField(max_length=200)
    razao_social = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=200)
    rg_ie = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    fax = models.CharField(max_length=200)
    tel = models.CharField(max_length=200)
    email = models.EmailField()
    #uuid = models.CharField(default='-- -- --', max_length=300)
    #url = models.URLField(default='-- -- --', max_length=300)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """
        TIPO_PESSOA = ['Fisica', 'Juridica']
        ESTADO = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
                "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                ]

        if self.tipo_pessoa not in TIPO_PESSOA:
            raise Exception('Campo Inválido!')
        if self.estado not in ESTADO:
            raise Exception('Campo Inválido!')
        #self.url = f'/fornecedor/details/{self.uuid}/'
        super(Fornecedor, self).save(*args, **kwargs)


class Produto(models.Model):
    # id_produto = models.IntegerField()
    cod_bar = models.CharField(max_length=200)
    data_cadastro = models.DateField()
    descricao = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    #custo = models.DecimalField(max_digits=12, decimal_places=2)
    #venda = models.DecimalField(max_digits=12, decimal_places=2)
    #lucro = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    #estoque = models.PositiveIntegerField()
    #uuid = models.CharField(default='-- -- --', max_length=300)
    #url = models.URLField(default='-- -- --', max_length=300)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """
        try:
            super(Produto, self).save(*args, **kwargs)
        except e:
            raise(e)

class Agendamentos(models.Model): 
    proprietario = models.CharField(max_length=80)
    animal   = models.CharField(max_length=60)
    telefone = models.CharField(max_length=60)
    email    = models.EmailField()
    
    #Serviços
    #servico = models.CharField(max_length=50,on)
    servico = models.ForeignKey('Servicos',on_delete=models.CASCADE,related_name='servico')
    serv_desc = models.CharField(max_length=50,default="")

    #Agendamento
    data = models.DateField()
    dia  = models.CharField(max_length=10)
    hora = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        dias = {
                "SUNDAY":"DOMINGO",
                "MONDAY":"SEGUNDA", 
                "TUESDAY":"TERCA",
                "WEDNESDAY":"QUARTA",
                "THURSDAY":"QUINTA", 
                "FRIDAY":"SEXTA", 
                "SATURDAY":"SABADO"
                }

        servicos_all = Servicos.objects.all().order_by('-id')  

        if not self.proprietario:
            raise Exception('Campo proprietario invalido !')
        if not self.animal:
            raise Exception('Campo animal invalido !')        
        if not self.telefone:
            raise Exception('Campo telefone invalido !')
        if not self.email:
            raise Exception('Campo e-mail invalido !')   

        if self.servico not in servicos_all:
            raise Exception('Serviço inválido')
        
        self.dia = dias[self.dia.strip().upper()]

        super(Agendamentos, self).save(*args, **kwargs)


class Servicos(models.Model):
    descricao = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.descricao:
            raise Exception('Campo descricao precisa ser preenchido !')
            
        super(Servicos, self).save(*args, **kwargs)

class Pedido(models.Model):
    cliente = models.IntegerField()
    cpf_cnpj = models.CharField(max_length=14)
    tipo  = models.CharField(max_length=20) #Venda ou Compra
    emissao = models.DateField(default=timezone.now)
    pagamento = models.ForeignKey('Tipos_pagamento',on_delete=models.CASCADE,) 
    forma_pagamento = models.CharField(max_length=60)
    vendedor  = models.CharField(max_length=150)
    observacao = models.CharField(max_length=200)     
    efetivado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        clientes = Cliente.objects.all().order_by('-id')  

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.cliente:
            raise Exception('Campo cliente invalido !')

            
        super(Pedido, self).save(*args, **kwargs)

class Itens_pedido(models.Model):
    
    TIPOS = [('P','S')]

    #tipo = models.CharField(max_length=14, choices=TIPOS, blank=False)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE,)
    descricao = models.CharField(max_length=150, blank=False) 
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2,blank=False)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    pedido = models.ForeignKey('Pedido',on_delete=models.CASCADE,)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        if not self.valor_unitario:
            raise Exception('Campo valor_unitario invalido !')
        if not self.quantidade:
            raise Exception('Campo quantidade invalido !')
        if not self.valor_total:
            raise Exception('Campo valor_total invalido !')
        super(Itens_pedido, self).save(*args, **kwargs)

class Estoque(models.Model):
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE,related_name='produto')
    quantidade = models.IntegerField()

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.quantidade:
            raise Exception('Campo quantidade invalido !')
        
        if Produto.objects.get(pk=self.produto_id) == None:
            raise Exception('Produto inválido')
            
        super(Estoque, self).save(*args, **kwargs)


class Entrada(models.Model):
    Pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE,related_name='pedido_entrada')
    fornece = models.ForeignKey(Fornecedor,on_delete=models.CASCADE,related_name='cliente_entrada')
    fornece_nome = models.CharField(max_length=200)
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE,related_name='produto_entrada')
    produto_descricao = models.CharField(max_length=250)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2,blank=False)
    valor_total    = models.DecimalField(max_digits=12, decimal_places=2,blank=False)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.quantidade:
            raise Exception('Campo quantidade invalido !')
        
        if Produto.objects.get(pk=self.produto_id) == None:
            raise Exception('Produto inválido')

        super(Entrada, self).save(*args, **kwargs)


class Saida(models.Model):
    Pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE,related_name='pedido_saida')
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,related_name='cliente')
    cliente_nome = models.CharField(max_length=200)
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE,related_name='prod')
    produto_descricao = models.CharField(max_length=250)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2,blank=False)
    valor_total    = models.DecimalField(max_digits=12, decimal_places=2,blank=False)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.quantidade:
            raise Exception('Campo quantidade invalido !')
        
        if Produto.objects.get(pk=self.produto_id) == None:
            raise Exception('Produto inválido')

        super(Saida, self).save(*args, **kwargs)


class Tipos_pagamento(models.Model):
    descricao = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """

        #produto = Produto.objects.get(id=self.id_produto)
        if not self.descricao:
            raise Exception('Campo descrição não pode ser vazio!')

        super(Tipos_pagamento, self).save(*args, **kwargs)    