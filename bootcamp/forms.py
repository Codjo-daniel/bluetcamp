from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class HomePageForm(forms.Form):
    email = forms.EmailField(label=False)


class CriarContaForm(UserCreationForm):
    #Campos desejados, e adicionais aos campos padrão
    # do formulario de criação de usuario padrão do Django
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')