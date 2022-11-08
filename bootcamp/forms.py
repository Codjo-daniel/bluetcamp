from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms
from django.core.mail.message import EmailMessage


class HomePageForm(forms.Form):
    email = forms.EmailField(label=False)


class CriarContaForm(UserCreationForm):
    #Campos desejados, e adicionais aos campos padrão
    # do formulario de criação de usuario padrão do Django
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.CharField(label='E-mail', max_length=100)
    assunto = forms.CharField(label='Assunto', max_length=100)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject=assunto,
            body=conteudo,
            from_email='contato@bluetcamp.com.br',
            to=['contato@bluetcamp.com.br',],
            headers={'Reply-To': email}
        )
        mail.send()
