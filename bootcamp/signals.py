from django.db.models.signals import post_save
from bootcamp.models import Usuario, Matricula, Bootcamp, Usuario_Interesse

def matricula_usuario(sender, instance, created, **kwargs):
    #print(f'Usuário logado: {instance.username}, email: {instance.email}')
    bootDesc = Usuario_Interesse.objects.filter(email=instance.email).filter(aprovado=True).first()

    if bootDesc:
        print(f'Bootcamp Interessado: {bootDesc.bootcamp_titulo}')
        boot = Bootcamp.objects.filter(titulo=bootDesc.bootcamp_titulo).first()

        mat = Matricula.objects.filter(usuario=instance).filter(bootcamp=boot).first()

        if boot:
            if created:
                if bootDesc:
                    Matricula.objects.create(usuario=instance, bootcamp=boot)
            else:
                if not mat:
                    Matricula.objects.create(usuario=instance, bootcamp=boot)


post_save.connect(matricula_usuario, sender=Usuario)

