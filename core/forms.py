from django.forms import ModelForm
from core.models import *


class CadastroPrestadorForm(ModelForm):
    class Meta:
        model = Prestador
        fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil', 'user']     