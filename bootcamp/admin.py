from django.contrib import admin
from .models import Bootcamp, Conteudo, Usuario, Modulo_usu_acomp, Usuario_Interesse
from .models import Modulo, Conteudo_Modulo, Modulo_Bootcamp, Conteudo_usu_acomp, Matricula
from django.contrib.auth.admin import UserAdmin


#<<Trecho para visualizar os campos distintos no Admin
campos = list(UserAdmin.fieldsets)
campos.append(
    ("histórico", {'fields': ('bootcamps_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)

class BootcampAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'categoria', 'data_evento')
    list_editable = ('publicado',)

class ConteudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo')

#Trecho para visualizar os campos distintos no Admin>>

# Register your models here.
admin.site.register(Bootcamp, BootcampAdmin)
admin.site.register(Modulo)
admin.site.register(Modulo_Bootcamp)
admin.site.register(Conteudo_Modulo)
admin.site.register(Conteudo, ConteudoAdmin)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Matricula)
admin.site.register(Conteudo_usu_acomp)
admin.site.register(Modulo_usu_acomp)
admin.site.register(Usuario_Interesse)

