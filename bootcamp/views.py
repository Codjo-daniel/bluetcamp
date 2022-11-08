from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CriarContaForm, HomePageForm, ContatoForm
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Bootcamp, Usuario, Modulo_Bootcamp, Conteudo, Conteudo_usu_acomp, Matricula
from django.contrib.auth.mixins import LoginRequiredMixin



class Homepage(FormView):
    template_name = "homepage.html"
    form_class = HomePageForm

    def get(self, request, *args, **kwargs):
        #Se o usuário estiver autenticado:
        if request.user.is_authenticated:
            #Redireciona o usuário para a Home Bootcamps
            return redirect('bootcamp:home_bootcamps')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email_acesso = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email_acesso)
        if usuarios:
            return reverse('bootcamp:login')
        else:
            return reverse('bootcamp:criar_conta')

class Home_bootcamps(LoginRequiredMixin, ListView):
    template_name = "home_bootcamps.html"
    model = Bootcamp
    #Object_List


class Detalhesbootcamp(LoginRequiredMixin, DetailView):
    template_name = "detalhes_bootcamp.html"
    model = Bootcamp
    #object -> item do modelo

    def __init__(self) -> None:
        self.user = None
        super().__init__()

    def get(self, request, *args, **kwargs):
        # 1 - descobrir qual bootcamp ele está acessando
        bootcamp = self.get_object()
        # 2 - Somar 1 visualização
        bootcamp.visualizacoes += 1
        # 3 - Salvar a visualização na base
        bootcamp.save()
        usuario = request.user
        usuario.bootcamps_vistos.add(bootcamp)
        self.user = request.user
        return super().get(request, *args, **kwargs) #redireciona o user para a url final

    def get_context_data(self, **kwargs):
        bootcamp = self.get_object()
        context = super(Detalhesbootcamp, self).get_context_data(**kwargs)
        #Filtrar os bootcamps de mesma categoria para listar
        bootcamps_relacionados = Bootcamp.objects.filter(categoria=self.get_object().categoria)[0:5]
        # Filtrar os módulos relacionados ao bootcamp selecionado, listando de forma ordenada
        modulos_ordenados = Modulo_Bootcamp.objects.filter(bootcamp=self.get_object().id).order_by('ordem')

        #Obter a informação se o usuário está cadastrado naquele bootcamp
        bootcamps_usuario = Matricula.objects.filter(usuario=self.user.id, bootcamp=bootcamp)
        #Transforma a informação do bootusuário de query em lista
        pode_ver_bootcamp = list(bootcamps_usuario)
        #Gera a informação de Verdade ou Falso do usuário estar no bootcamp
        context['pode_ver_bootcamp'] = bool(pode_ver_bootcamp)
        context['bootcamps_relacionados'] = bootcamps_relacionados
        context['modulos_ordenados'] = modulos_ordenados
        return context

class DetalheConteudo(LoginRequiredMixin, DetailView):
    template_name = "detalhe_conteudo.html"
    model = Conteudo
    #object -> item do modelo

    def get(self, request, *args, **kwargs):
        # 1 - descobrir qual bootcamp ele está acessando
        conteudo = self.get_object()
        #print(conteudo)
        usuario = request.user
        #print(usuario.username)
        usuario.conteudos_vistos.add(conteudo)
        return super().get(request, *args, **kwargs) #redireciona o user para a url final

class PesquisaBootcamp(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Bootcamp

    #Object_List (Editando a lista do objeto com o resultado pesquisado)
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class PaginaPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editar_perfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('bootcamp:home_bootcamps')


class CriarConta(FormView):
    template_name = "criar_conta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bootcamp:login')

class Contato(LoginRequiredMixin, FormView):
    template_name = "contato.html"
    form_class = ContatoForm
    #sucess_url = reverse_lazy('contato')

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(Contato, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(Contato, self).form_invalid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse('bootcamp:home_bootcamps')


