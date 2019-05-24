from django.db import models

class Cliente(models.Model):
    tipo_pessoa = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=200)
    rg = models.CharField(max_length=200)
    email = models.EmailField()
    estado_civil = models.CharField(max_length=200)
    data_nasc = models.DateField()
    cep = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    tipo_tel = models.CharField(max_length=200)
    tel = models.CharField(max_length=200)
    uuid = models.CharField(default='-- -- --', max_length=300)
    url = models.URLField(default='-- -- --', max_length=300)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """
        TIPO_PESSOA = ['Fisica', 'Juridica']
        SEXO = ['Masculino', 'Feminino']
        ESTADO_CIVIL = [
                        'Solteiro(a)',
                        'Casado(a)',
                        'Divorciado(a)',
                        'Viúvo(a)'
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
        if self.estado_civil not in ESTADO_CIVIL:
            raise Exception('Campo Estado Civil Inválido!')
        if self.estado not in ESTADO:
            raise Exception('Campo Estado Inválido!')
        if self.tipo_tel not in TIPO_TEL:
            raise Exception('Campo Tipo de Telefone Inválido!')
        self.url = f'/cliente/details/{self.uuid}/'
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
    uuid = models.CharField(default='-- -- --', max_length=300)
    url = models.URLField(default='-- -- --', max_length=300)

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
        self.url = f'/fornecedor/details/{self.uuid}/'
        super(Fornecedor, self).save(*args, **kwargs)

class Produto(models.Model):
    id_fornecedor = models.IntegerField()
    cod_bar = models.CharField(max_length=200, unique=True)
    data_cadastro = models.DateField()
    descricao = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    custo = models.DecimalField(max_digits=12, decimal_places=2)
    venda = models.DecimalField(max_digits=12, decimal_places=2)
    lucro = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    estoque = models.PositiveIntegerField()
    uuid = models.CharField(default='-- -- --', max_length=300)
    url = models.URLField(default='-- -- --', max_length=300)

    def save(self, *args, **kwargs):
        """
        Validação do objeto.
        """
        fornecedor = Fornecedor.objects.get(id=self.id_fornecedor)
        if not fornecedor:
            raise Exception('Campo id do fornecedor inválido!')
        if self.lucro == 0.00:
            self.lucro = self.venda - self.custo
        self.url = f'/produto/details/{self.uuid}/'
        super(Produto, self).save(*args, **kwargs)
