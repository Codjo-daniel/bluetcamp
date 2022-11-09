from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


LISTA_CATEGORIAS = (
    ("ENGENHARIA DE DADOS","Engenharia de Dados"),
    ("CIÊNCIA DE DADOS","Ciência de Dados"),
    ("VISUALIZAÇÃO DE DADOS", "Visualização de Dados"),
    ("OUTROS","Outros")
)

LISTA_CATEGORIAS_MODULOS = (
    ("PROGRAMAÇÃO","Programação"),
    ("BANCO DE DADOS","Banco de Dados"),
    ("IA", "Machine/Deep Learn"),
    ("VISUALIZAÇÃO DE DADOS","Visualização de Dados"),
    ("OUTROS","Outros")
)

TIPOS_CONTEUDO = (
    ("STREAMING","Video Streaming (Youtube)"),
    ("DOCUMENTOS","Documentos PDF"),
    ("VIDEO", "Arquivos de Vídeo (mp4)"),
    ("PROVA", "Link de Avaliação de Módulo")
)

TIPOS_GENERO = (
    ("HOMEM CIS","Homem Cis"),
    ("MULHER CIS","Mulher Cis"),
    ("HOMEM TRANS","Homem Trans"),
    ("MULHER TRANS","Mulher Trans"),
    ("TRAVESTI","Travesti"),
    ("NAO BINARIO","Não Binário"),
    ("OUTROS","Outros"),
    ("NAO INFORMADO","Não quero Informar")
)

# Criar o Bootcamp
class Bootcamp(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=150, unique=True)
    thumb = models.ImageField(upload_to='thumb_app')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=150, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(default=timezone.now)
    data_evento = models.DateTimeField()
    publicado = models.BooleanField(default=False)
    link_interesse = models.URLField(blank=True, default=None, null=True)

    class Meta:
        db_table = 'bootcamp'

    def __str__(self):
        return self.titulo


class Modulo(models.Model):
    id = models.IntegerField(primary_key=True)
    mod_descricao = models.CharField(max_length=255)
    mod_categoria = models.CharField(max_length=150, choices=LISTA_CATEGORIAS_MODULOS)
    bootcamps = models.ManyToManyField("Bootcamp", blank=True, through='Modulo_Bootcamp')

    class Meta:
        db_table = 'modulo'

    def __str__(self):
        return self.mod_descricao

class Modulo_Bootcamp(models.Model):
    id = models.IntegerField(primary_key=True)
    bootcamp = models.ForeignKey("Bootcamp", related_name="bootcamps_modulo", on_delete=models.CASCADE)
    modulo = models.ForeignKey("Modulo", related_name="modulos", on_delete=models.CASCADE)
    ordem = models.IntegerField(default=0)

    class Meta:
        db_table = 'modulo_bootcamp'

    def __str__(self):
        return self.bootcamp.titulo + " - " + self.modulo.mod_descricao


class Conteudo(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=150)
    caminho = models.URLField()
    tipo = models.CharField(max_length=150, choices=TIPOS_CONTEUDO, default="")
    modulos = models.ManyToManyField("Modulo", blank=True, through='Conteudo_Modulo')

    class Meta:
        db_table = 'conteudo'

    def __str__(self):
        return self.titulo

class Conteudo_Modulo(models.Model):
    id = models.IntegerField(primary_key=True)
    modulo = models.ForeignKey("Modulo", related_name="modulos_conteudo", on_delete=models.CASCADE)
    conteudo = models.ForeignKey("Conteudo", related_name="conteudos", on_delete=models.CASCADE)
    ordem = models.IntegerField(default=0)

    class Meta:
        db_table = 'conteudo_modulo'

    def __str__(self):
        return self.modulo.mod_descricao + " - " + self.conteudo.titulo


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    bootcamps_vistos = models.ManyToManyField("Bootcamp", blank=True)
    conteudos_vistos = models.ManyToManyField("Conteudo", blank=True, through='Conteudo_usu_acomp')
    modulos_vistos = models.ManyToManyField("Modulo", blank=True, through='Modulo_usu_acomp')
    email = models.EmailField(max_length=255, unique=True)

    class Meta:
        db_table = 'usuario'


class Matricula(models.Model):
    id = models.AutoField(primary_key=True)
    bootcamp = models.ForeignKey("Bootcamp", related_name="bootcamps_matricula", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", related_name="usuarios_matriculados", on_delete=models.CASCADE)
    mat_data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'matricula'

    def __str__(self):
        return self.bootcamp.titulo + " - " + self.usuario.username



class Conteudo_usu_acomp(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey("Usuario", related_name="usuarios_acomp", on_delete=models.CASCADE)
    conteudo = models.ForeignKey("Conteudo", related_name="conteudos_consumidos", on_delete=models.CASCADE)
    coa_data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'conteudo_usu_acomp'

    def __str__(self):
        return self.usuario.username + " - " + self.conteudo.titulo


class Modulo_usu_acomp(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey("Usuario", related_name="usuarios_modulos_acomp", on_delete=models.CASCADE)
    modulo = models.ForeignKey("Modulo", related_name="modulos_consumidos", on_delete=models.CASCADE)
    moa_data_ini = models.DateTimeField(default=timezone.now)
    moa_data_fim = models.DateTimeField(blank=True, default=None, null=True)

    class Meta:
        db_table = 'modulo_usu_acomp'

    def __str__(self):
        return self.usuario.username + " - " + self.modulo.mod_descricao

# Usuários interessados - preenchidos pelo Microsoft Forms
class Usuario_Interesse(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150, blank=True, default=None, null=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    data_nascimento = models.DateTimeField(blank=True, default=None, null=True)
    genero = models.CharField(max_length=150, choices=TIPOS_GENERO, blank=True, default=None, null=True)
    email = models.CharField(max_length=150, blank=True, default=None, null=True)
    telefone = models.CharField(max_length=30, blank=True, default=None, null=True)
    estado = models.CharField(max_length=5, blank=True, default=None, null=True)
    cidade = models.CharField(max_length=100, blank=True, default=None, null=True)
    lgpd = models.CharField(max_length=30, blank=True, default=None, null=True)
    veracidade = models.BooleanField(default=False, blank=True, null=True)
    receber_mensagens = models.BooleanField(default=False, blank=True, null=True)
    aprovado = models.BooleanField(default=False, blank=True, null=True)
    bootcamp_titulo = models.CharField(max_length=150, blank=True, default=None, null=True)

    class Meta:
        db_table = 'usuario_interesse'

    def __str__(self):
        return self.nome


