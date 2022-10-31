from django.contrib import admin
from .models import Bootcamp, Conteudo, Usuario
from django.contrib.auth.admin import UserAdmin


#<<Trecho para visualizar os campos distintos no Admin
campos = list(UserAdmin.fieldsets)
campos.append(
    ("histórico", {'fields': ('bootcamps_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)
#Trecho para visualizar os campos distintos no Admin>>

# Register your models here.
admin.site.register(Bootcamp)
admin.site.register(Conteudo)
admin.site.register(Usuario, UserAdmin)


