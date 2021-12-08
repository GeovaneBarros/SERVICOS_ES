from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages

# Create your views here.
from core.models import *
class SobreTemplateView(TemplateView):
    template_name = './sobre/sobre.html'

class UsuarioCreateView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = './usuario/criar.html'
    success_url = reverse_lazy('sobre_template_view')


@method_decorator(login_required, name='dispatch')
class PrestadorCreateView(CreateView):
    model = Prestador
    template_name = './prestador/criar.html'
    fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil']
    success_url = reverse_lazy('sobre_template_view')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(PrestadorCreateView, self).form_valid(form)

class PrestadorListView(ListView):
    model = Prestador
    template_name = './prestador/listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestadores'] = Prestador.objects.all() 
        return context


class PrestadorDetailView(DetailView):
    context_object_name = 'prestador'
    queryset = Prestador.objects.all()
    template_name = './prestador/detalhe.html'


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render('dashboard/index.html')
        return render(request, self.template_name)
    
    def post(self, request):
        post = request.POST
        username = post.get('username')
        password = post.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard_view')
        messages.info(request, 'Email ou senha incorretos')
