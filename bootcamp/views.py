from django.shortcuts import render, redirect, reverse
from .forms import CriarContaForm, HomePageForm
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Bootcamp, Usuario
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

    def get(self, request, *args, **kwargs):
        # 1 - descobrir qual bootcamp ele está acessando
        bootcamp = self.get_object()
        # 2 - Somar 1 visualização
        bootcamp.visualizacoes += 1
        # 3 - Salvar a visualização na base
        bootcamp.save()
        usuario = request.user
        usuario.bootcamps_vistos.add(bootcamp)
        return super().get(request, *args, **kwargs) #redireciona o user para a url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesbootcamp, self).get_context_data(**kwargs)
        #Filtrar os bootcamps de mesma categoria para listar
        bootcamps_relacionados = Bootcamp.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['bootcamps_relacionados'] = bootcamps_relacionados
        return context

class PesquisaBootcamp(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Bootcamp

    #Object_List (Eitando a lista do objeto com o resultado pesquisado)
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
