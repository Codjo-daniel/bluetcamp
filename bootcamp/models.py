from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


LISTA_CATEGORIAS = (
    ("ENGENHARIA DE DADOS","Engenharia de Dados"),
    ("CIÊNCIA DE DADOS","Ciência de Dados"),
    ("VISUALIZAÇÃO DE DADOS", "Visualização de Dados"),
    ("OUTROS","Outros")
)


# Criar o Bootcamp
class Bootcamp(models.Model):
    titulo = models.CharField(max_length=150)
    thumb = models.ImageField(upload_to='thumb_bootcamp')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=50, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(default=timezone.now)
    data_evento = models.DateTimeField()

    def __str__(self):
        return self.titulo

class Conteudo(models.Model):
    bootcamp = models.ForeignKey("Bootcamp", related_name="conteudos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    caminho = models.URLField()

    def __str__(self):
        return self.bootcamp.titulo + " - " + self.titulo


class Usuario(AbstractUser):
    bootcamps_vistos = models.ManyToManyField("Bootcamp")