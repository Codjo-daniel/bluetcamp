from .models import Bootcamp


def lista_bootcamps_recentes(request):
    list_bootcamps_recentes = Bootcamp.objects.all().order_by('-data_cadastro')[0:8]
    return {"lista_bootcamps_recentes": list_bootcamps_recentes}

def lista_bootcamps_populares(request):
    list_bootcamps_emalta = Bootcamp.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_bootcamps_populares": list_bootcamps_emalta}

def retorna_bootcamp_destaque(request):
    boots_destaque = Bootcamp.objects.all().order_by('data_evento')
    if boots_destaque:
        boot_destaque = boots_destaque[0]
    else:
        boot_destaque = None
    return {"boot_destaque": boot_destaque}