from django.urls import path, reverse_lazy
from .views import Homepage, Home_bootcamps, Detalhesbootcamp, PesquisaBootcamp
from .views import PaginaPerfil, CriarConta, DetalheConteudo, Contato
from django.contrib.auth import views as auth_view

app_name = 'bootcamp'


urlpatterns = [
    path("", Homepage.as_view(), name='homepage'),
    path("bootcamps/", Home_bootcamps.as_view(), name='home_bootcamps'),
    path("bootcamps/<int:pk>", Detalhesbootcamp.as_view(), name='detalhes_bootcamp'),
    path("conteudo/<int:pk>", DetalheConteudo.as_view(), name='detalhe_conteudo'),
    path("pesquisa/", PesquisaBootcamp.as_view(), name='pesquisabootcamp'),
    path("login/", auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path("editarperfil/<int:pk>", PaginaPerfil.as_view(), name='editar_perfil'),
    path("criarconta/", CriarConta.as_view(), name='criar_conta'),
    path("mudarsenha/", auth_view.PasswordChangeView.as_view(template_name='editar_perfil.html',
                                                             success_url=reverse_lazy('bootcamp:home_bootcamps')), name='mudar_senha'),
    path("contato/", Contato.as_view(), name='contato'),

]