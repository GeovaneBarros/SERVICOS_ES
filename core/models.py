from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

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


class Servico(models.Model):
    nome = models.CharField(max_length=256)
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    descricao = models.TextField(max_length=1000)
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
    
    def __str__(self) -> str:
        return (self.nome+' '+self.preco)

class Avaliacao(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=1000)
    nota = models.IntegerField()
    whatsapp = models.CharField(max_length=20)
    anonimo = models.BooleanField()

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    
    def __str__(self) -> str:
        return (self.prestador+' '+self.nota)
