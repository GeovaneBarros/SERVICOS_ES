from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Prestador(models.Model):
    nome = models.CharField(max_length=64)
    ramo = models.CharField(max_length=64)
    whatsapp = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField()

    class Meta:
        verbose_name = 'Prestador'
        verbose_name_plural = 'Prestadores'
    
    def __str__(self) -> str:
        return self.nome

class Endereco(models.Model):
    rua = models.CharField(max_length=128)
    numero = models.CharField(max_length=8)
    bairro = models.CharField(max_length=64)
    cidade = models.CharField(max_length=32)
    estado = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
    
    def __str__(self) -> str:
        return (self.rua+self.numero)